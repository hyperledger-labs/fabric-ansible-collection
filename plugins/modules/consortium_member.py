#!/usr/bin/python
#
# SPDX-License-Identifier: Apache-2.0
#

from __future__ import absolute_import, division, print_function
__metaclass__ = type

from ..module_utils.channel_utils import get_highest_capability
from ..module_utils.dict_utils import equal_dicts, merge_dicts, copy_dict
from ..module_utils.module import BlockchainModule
from ..module_utils.msp_utils import organization_to_msp
from ..module_utils.proto_utils import proto_to_json, json_to_proto
from ..module_utils.utils import get_console, get_organization_by_module

from ansible.module_utils._text import to_native

import json

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = '''
---
module: consortium_member
short_description: Manage a consortium member for a Hyperledger Fabric ordering service
description:
    - Add, update, and remove consortium members for a Hyperledger Fabric ordering service.
    - This module works with the IBM Support for Hyperledger Fabric software or the Hyperledger Fabric
      Open Source Stack running in a Red Hat OpenShift or Kubernetes cluster.
author: Simon Stone (@sstone1)
options:
    api_endpoint:
        description:
            - The URL for the Fabric operations console.
        type: str
        required: true
    api_authtype:
        description:
            - C(basic) - Authenticate to the Fabric operations console using basic authentication.
              You must provide both a valid API key using I(api_key) and API secret using I(api_secret).
        type: str
        required: true
    api_key:
        description:
            - The API key for the Fabric operations console.
        type: str
        required: true
    api_secret:
        description:
            - The API secret for the Fabric operations console.
            - Only required when I(api_authtype) is C(basic).
        type: str
    api_timeout:
        description:
            - The timeout, in seconds, to use when interacting with the Fabric operations console.
        type: int
        default: 60
    state:
        description:
            - C(absent) - An organization matching the specified name will be removed from the consortium.
            - C(present) - Asserts that an organization matching the specified name and configuration exists
              in the consortium. If no organization matches the specified name, the organization will be added
              to the consortium. If an organization matches the specified name but the configuration does not
              match, then the organization in the consortium will be updated.
        type: str
        default: present
        choices:
            - absent
            - present
    path:
        description:
            - Path to current the system channel configuration file.
            - This file can be fetched by using the M(channel_config) module.
            - This file will be updated in place. You will need to keep a copy of the original file for computing the configuration
              update.
        type: str
        required: true
    organization:
        description:
            - The organization to add, update, or remove from the consortium.
            - You can pass a string, which is the display name of an organization registered
              with the Fabric operations console.
            - You can also pass a dictionary, which must match the result format of one of the
              M(organization_info) or M(organization[]) modules.
        type: raw
        required: true
    policies:
        description:
            - The set of policies for the consortium member. The keys are the policy
              names, and the values are the policies.
            - You can pass strings, which are paths to JSON files containing policies
              in the Hyperledger Fabric format (common.Policy).
            - You can also pass a dict, which must correspond to a parsed policy in the
              Hyperledger Fabric format (common.Policy).
            - Default policies are provided for the Admins, Writers, Readers, and Endorsement
              policies. You only need to provide policies if you want to override these default
              policies, or add additional policies.
        type: dict
notes: []
requirements: []
'''

EXAMPLES = '''
- name: Add the organization to the consortium
  hyperledger.fabric_ansible_collection.consortium_member:
    state: present
    api_endpoint: https://console.example.org:32000
    api_authtype: basic
    api_key: xxxxxxxx
    api_secret: xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    organization: Org1
    path: channel_config.bin

- name: Remove the organization from the consortium
  hyperledger.fabric_ansible_collectionble-collectionble-collectionble-collection.consortium_member:
    state: absent
    api_endpoint: https://console.example.org:32000
    api_authtype: basic
    api_key: xxxxxxxx
    api_secret: xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    organization: Org1
    path: channel_config.bin
'''

RETURN = '''
---
{}
'''


def main():

    # Create the module.
    argument_spec = dict(
        state=dict(type='str', default='present', choices=['present', 'absent']),
        api_endpoint=dict(type='str', required=True),
        api_authtype=dict(type='str', choices=['ibmcloud', 'basic'], required=True),
        api_key=dict(type='str', no_log=True, required=True),
        api_secret=dict(type='str', no_log=True),
        api_timeout=dict(type='int', default=60),
        api_token_endpoint=dict(type='str', default='https://iam.cloud.ibm.com/identity/token'),
        path=dict(type='str', required=True),
        organization=dict(type='raw', required=True),
        policies=dict(type='dict', default=dict())
    )
    required_if = [
        ('api_authtype', 'basic', ['api_secret'])
    ]
    module = BlockchainModule(argument_spec=argument_spec, supports_check_mode=True, required_if=required_if)

    # Ensure all exceptions are caught.
    try:

        # Log in to the console.
        console = get_console(module)

        # Get the organization and the target path.
        path = module.params['path']
        organization = get_organization_by_module(console, module)

        # Get the policies.
        policies = module.params['policies']
        actual_policies = dict()
        for policyName, policy in policies.items():
            if isinstance(policy, str):
                with open(policy, 'r') as file:
                    actual_policies[policyName] = json.load(file)
            elif isinstance(policy, dict):
                actual_policies[policyName] = policy
            else:
                raise Exception(f'The policy {policyName} is invalid')

        # Read the config.
        with open(path, 'rb') as file:
            config_json = proto_to_json('common.Config', file.read())

        # Determine the capabilities for this channel.
        highest_capability = get_highest_capability(config_json['channel_group'])
        endorsement_policy_required = False
        if highest_capability is not None and highest_capability >= 'V2_0':
            endorsement_policy_required = True

        # Check to see if the consortium member exists.
        consortium_groups = config_json['channel_group']['groups']['Consortiums']['groups']['SampleConsortium']['groups']
        msp = consortium_groups.get(organization.msp_id, None)

        # Handle the desired state appropriately.
        state = module.params['state']
        if state == 'present' and msp is None:

            # Add the consortium member.
            msp = organization_to_msp(organization, endorsement_policy_required, actual_policies)
            consortium_groups[organization.msp_id] = msp

        elif state == 'present' and msp is not None:

            # Update the consortium member.
            new_msp = organization_to_msp(organization, endorsement_policy_required, actual_policies)
            updated_msp = copy_dict(msp)
            merge_dicts(updated_msp, new_msp)
            if equal_dicts(msp, updated_msp):
                return module.exit_json(changed=False)
            consortium_groups[organization.msp_id] = updated_msp

        elif state == 'absent' and msp is None:

            # Nothing to do.
            return module.exit_json(changed=False)

        elif state == 'absent' and msp is not None:

            # Delete the consortium member.
            del consortium_groups[organization.msp_id]

        # Save the config.
        config_proto = json_to_proto('common.Config', config_json)
        with open(path, 'wb') as file:
            file.write(config_proto)
        module.exit_json(changed=True)

    # Notify Ansible of the exception.
    except Exception as e:
        module.fail_json(msg=to_native(e))


if __name__ == '__main__':
    main()
