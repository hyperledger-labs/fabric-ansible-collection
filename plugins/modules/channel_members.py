#!/usr/bin/python
#
# SPDX-License-Identifier: Apache-2.0
#

from __future__ import absolute_import, division, print_function
__metaclass__ = type

from ..module_utils.module import BlockchainModule
from ..module_utils.proto_utils import proto_to_json, json_to_proto
from ..module_utils.dict_utils import copy_dict

from ansible.module_utils._text import to_native

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = '''
---
module: channel_members
short_description: Manage anchor peers for a channel
description:
    - Manage anchor peers for the whole channel.
    - Migrate anchor peer addresses to the newer open source format
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
    path:
        description:
            - Path to current the channel configuration file.
            - This file can be fetched by using the M(channel_config) module.
            - This file will be updated in place. You will need to keep a copy of the original file for computing the configuration
              update.
        type: str
        required: true
    operation:
        description:
            - C(migrate_addresses_to_os) - Convert the anchor peer addresses in the channel to open source standards
        type: str
        required: true
notes: []
requirements: []
'''

EXAMPLES = '''
- name: Add the organization to the channel
  hyperledger.fabric_ansible_collection.channel_member:
    state: present
    api_endpoint: https://console.example.org:32000
    api_authtype: basic
    api_key: xxxxxxxx
    api_secret: xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    path: updated_config.bin
    operation: 'migrate_addresses_to_os'
'''

RETURN = '''
---
{}
'''


def migrate_addresses_to_os(module):

    changed = False

    # Get the organization and the target path.
    path = module.params['path']

    # Read the config.
    with open(path, 'rb') as file:
        config_json = proto_to_json('common.Config', file.read())

    original_config_json = copy_dict(config_json)

    # check to see if this is a system channel
    if 'Consortiums' in config_json['channel_group']['groups']:
        module.exit_json(changed=changed, msps=None, original_config_json=None, updated_config_json=None)

    # Check to see if the channel member exists.
    application_groups = config_json['channel_group']['groups']['Application']['groups']

    organizations = list()

    for msp_id in application_groups:

        msp = config_json['channel_group']['groups']['Application']['groups'][msp_id]

        anchor_peers_value = msp['values']['AnchorPeers']['value']['anchor_peers']

        for idx, anchor_peer in enumerate(anchor_peers_value):

            old_hostname = anchor_peer['host'].split(".")

            if not old_hostname[0].endswith('-peer'):
                old_hostname[0] = old_hostname[0] + '-peer'
                new_host_name = '.'.join(str(hostname_part) for hostname_part in old_hostname)
                anchor_peers_value[idx]['host'] = new_host_name
                changed = True

            if anchor_peer['port'] != 443:
                anchor_peers_value[idx]['port'] = 443
                changed = True

        if changed:
            organizations.append(msp_id)

    # Save the config.
    config_proto = json_to_proto('common.Config', config_json)
    with open(path, 'wb') as file:
        file.write(config_proto)
    module.exit_json(changed=changed, organizations=organizations, original_config_json=original_config_json, updated_config_json=config_json)


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
        operation=dict(type='str', required=True, choices=['migrate_addresses_to_os'])
    )
    required_if = [
        ('api_authtype', 'basic', ['api_secret']),
        ('operation', 'migrate_addresses_to_os', ['api_endpoint', 'api_authtype', 'api_key', 'path'])
    ]
    module = BlockchainModule(argument_spec=argument_spec, supports_check_mode=True, required_if=required_if)

    # Ensure all exceptions are caught.
    try:
        operation = module.params['operation']
        if operation == 'migrate_addresses_to_os':
            migrate_addresses_to_os(module)
        else:
            raise Exception(f'Invalid operation {operation}')

    # Notify Ansible of the exception.
    except Exception as e:
        module.fail_json(msg=to_native(e))


if __name__ == '__main__':
    main()
