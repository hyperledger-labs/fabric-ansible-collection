#!/usr/bin/python
#
# SPDX-License-Identifier: Apache-2.0
#

from __future__ import absolute_import, division, print_function
__metaclass__ = type

from ..module_utils.module import BlockchainModule
from ..module_utils.utils import get_console
from ..module_utils.dict_utils import (merge_dicts)

from ansible.module_utils._text import to_native

import json
import time

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
    name: Org1 CA
    action: renew
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
        action=dict(type='str', required=True, choices=['restart', 'renew']),
        wait_timeout=dict(type='int', default=600)
    )
    required_if = [
        ('api_authtype', 'basic', ['api_secret'])
    ]
    module = BlockchainModule(argument_spec=argument_spec, supports_check_mode=True, required_if=required_if)

    # Ensure all exceptions are caught.
    try:

        timeout = module.params['wait_timeout']

        # Log in to the console.
        console = get_console(module)

        # Determine if the certificate authority exists.
        certificate_authority = console.get_component_by_display_name('fabric-ca', module.params['name'], deployment_attrs='included')

        # save a copy of the existing tls-cert
        existing_tls_cert = certificate_authority['msp']['component']['tls_cert']

        # If it doesn't exist, return now.
        if certificate_authority is None:
            return module.exit_json(exists=False)

        # Initialize the action object
        action_obj = dict()

        # Initialize the restart object
        restart_obj = dict(
            restart=True
        )

        # Initialize the tls renew object
        renew_obj = dict(
            renew=dict(tls_cert=True)
        )

        if module.params['action'] == 'restart':
            merge_dicts(action_obj, restart_obj)

        if module.params['action'] == 'renew':
            merge_dicts(action_obj, renew_obj)

        accepted = False

        action_response = console.action_ca(certificate_authority['id'], action_obj)

        if action_response['message'] == 'accepted':
            accepted = True

            if module.params['action'] == 'renew':

                last_e = None
                renewed = False
                for x in range(timeout):
                    try:
                        certificate_authority = console.get_component_by_display_name('fabric-ca', module.params['name'], deployment_attrs='included')

                        tls_cert = certificate_authority['msp']['component']['tls_cert']

                        if existing_tls_cert != tls_cert:
                            renewed = True
                            break
                    except Exception as e:
                        last_e = e
                    time.sleep(1)

                if not renewed:
                    raise Exception(f'Certificate authority failed to renew the TLS certificate within {timeout} seconds: {str(last_e)}')

        # Return certificate authority information.
        module.exit_json(accepted=accepted, response=json.dumps(action_response))

    # Notify Ansible of the exception.
    except Exception as e:
        module.fail_json(msg=to_native(e))


if __name__ == '__main__':
    main()
