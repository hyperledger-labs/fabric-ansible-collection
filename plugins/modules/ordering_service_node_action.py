#!/usr/bin/python
#
# SPDX-License-Identifier: Apache-2.0
#

from __future__ import absolute_import, division, print_function
__metaclass__ = type

from ..module_utils.module import BlockchainModule
from ..module_utils.utils import get_console

from ansible.module_utils._text import to_native

import json

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = '''
---
module: certificate_authority_action
short_description: Get information about a Hyperledger Fabric certificate authority
description:
    - Get information about a Hyperledger Fabric certificate authority.
    - This module works with the IBM Support for Hyperledger Fabric software or the Hyperledger Fabric
      Open Source Stack running in a Red Hat OpenShift or Kubernetes cluster.
author: Simon Stone (@sstone1)
options:
    api_endpoint:
        description:
            - The URL for the the Fabric operations console.
        type: str
        required: true
    api_authtype:
        description:
            - C(basic) - Authenticate to the the Fabric operations console using basic authentication.
              You must provide both a valid API key using I(api_key) and API secret using I(api_secret).
        type: str
        required: true
    api_key:
        description:
            - The API key for the the Fabric operations console.
        type: str
        required: true
    api_secret:
        description:
            - The API secret for the the Fabric operations console.
            - Only required when I(api_authtype) is C(basic).
        type: str
    api_timeout:
        description:
            - The timeout, in seconds, to use when interacting with the the Fabric operations console.
        type: int
        default: 60
    name:
        description:
            - The name of the certificate authority.
        required: true
    action:
        description:
            - Action requested.  Must be restart, enroll or reenroll
        required: true
    type:
        description:
            - Type of enrollment or reenrollment.  Must be ecert or tls_cert
    wait_timeout:
        description:
            - The timeout, in seconds, to wait until the certificate authority is available.
        type: int
        default: 60
notes: []
requirements: []
'''

EXAMPLES = '''
- name: Get certificate authority
  hyperledger.fabric_ansible_collection.certificate_authority_action:
    api_endpoint: https://console.example.org:32000
    api_authtype: basic
    api_key: xxxxxxxx
    api_secret: xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    name: Ordering Service_1
    action: reenroll
    type: tls_cert
'''

RETURN = '''
---
exists:
    description:
        - True if the certificate authority exists, false otherwise.
    returned: always
    type: boolean
certificate_authority:
    description:
        - The certificate authority.
    returned: if certificate authority exists
    type: dict
    contains:
        name:
            description:
                - The name of the certificate authority.
            type: str
            sample: Org1 CA
        api_url:
            description:
                - The URL for the API of the certificate authority.
            type: str
            sample: https://org1ca-api.example.org:32000
        operations_url:
            description:
                - The URL for the operations service of the certificate authority.
            type: str
            sample: https://org1ca-operations.example.org:32000
        ca_url:
            description:
                - The URL for the API of the certificate authority.
            type: str
            sample: https://org1ca-api.example.org:32000
        ca_name:
            description:
                - The certificate authority name to use for enrollment requests.
            type: str
            sample: ca
        tlsca_name:
            description:
                - The certificate authority name to use for TLS enrollment requests.
            type: str
            sample: tlsca
        location:
            description:
                - The location of the certificate authority.
            type: str
            sample: ibmcloud
        pem:
            description:
                - The TLS certificate chain for the certificate authority.
                - The TLS certificate chain is returned as a base64 encoded PEM.
            type: str
            sample: LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0t...
        tls_cert:
            description:
                - The TLS certificate chain for the certificate authority.
                - The TLS certificate chain is returned as a base64 encoded PEM.
            type: str
            sample: LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0t...
'''


def main():

    # Create the module.
    argument_spec = dict(
        api_endpoint=dict(type='str', required=True),
        api_authtype=dict(type='str', required=True, choices=['ibmcloud', 'basic']),
        api_key=dict(type='str', required=True, no_log=True),
        api_secret=dict(type='str', no_log=True),
        api_timeout=dict(type='int', default=60),
        api_token_endpoint=dict(type='str', default='https://iam.cloud.ibm.com/identity/token'),
        name=dict(type='str', required=True),
        action=dict(type='str', required=True, choices=['restart', 'enroll', 'reenroll']),
        target=dict(type='str', choices=['ecert', 'tls_cert']),
        wait_timeout=dict(type='int', default=600)
    )
    required_if = [
        ('api_authtype', 'basic', ['api_secret'])
    ]
    module = BlockchainModule(argument_spec=argument_spec, supports_check_mode=True, required_if=required_if)

    # Ensure all exceptions are caught.
    try:

        # Log in to the console.
        console = get_console(module)

        # Determine if the certificate authority exists.
        ordering_service_node = console.get_component_by_display_name('fabric-orderer', module.params['name'], deployment_attrs='included')

        # If it doesn't exist, return now.
        if ordering_service_node is None:
            return module.exit_json(exists=False)

        # Initialize the action object
        action_obj = dict()

        if module.params['action'] == 'restart':
            action_obj['restart'] = True
        else:
            # Check to make sure the target is 'enroll' or 'reenroll'
            if module.params['target'] not in ['ecert', 'tls_cert']:
                raise Exception('Target must be ecert or tls_cert the enrollment or reenrollment action')

            action_obj[module.params['action']] = {}

            action_obj[module.params['action']][module.params['target']] = True

        accepted = False

        module.json_log({
            'msg': 'Ordering Node Action',
            'Action Object': action_obj
        })

        action_response = console.action_ordering_service_node(ordering_service_node['id'], action_obj)

        if action_response['message'] == 'accepted':
            accepted = True

        # Return certificate authority information.
        module.exit_json(accepted=accepted, response=json.dumps(action_response))

    # Notify Ansible of the exception.
    except Exception as e:
        module.fail_json(msg=to_native(e))


if __name__ == '__main__':
    main()
