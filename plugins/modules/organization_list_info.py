#!/usr/bin/python
#
# SPDX-License-Identifier: Apache-2.0
#

from __future__ import absolute_import, division, print_function
__metaclass__ = type

from ..module_utils.module import BlockchainModule
from ..module_utils.utils import get_console, get_all_organizations

from ansible.module_utils._text import to_native

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = '''
---
module: organization_list_info
short_description: Get information about all Hyperledger Fabric organizations
description:
    - Get information about all Hyperledger Fabric organizations.
    - This module works with the IBM Support for Hyperledger Fabric software or the Hyperledger Fabric
      Open Source Stack running in a Red Hat OpenShift or Kubernetes cluster.
author: Chris Elder
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
    wait_timeout:
        description:
            - The timeout, in seconds, to wait until the certificate authority is available.
        type: int
        default: 60
notes: []
requirements: []
'''

EXAMPLES = '''
- name: Get all organizations
  hyperledger.fabric_ansible_collection.organization_list_info:
    api_endpoint: https://console.example.org:32000
    api_authtype: basic
    api_key: xxxxxxxx
    api_secret: xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
'''

RETURN = '''
---
exists:
    description:
        - True if the certificate authority exists, false otherwise.
    returned: always
    type: boolean
organization:
    description:
        - The organization.
    returned: if organization exists
    type: dict
    contains:
        name:
            description:
                - The name of the organization.
            type: str
            sample: Org1
        msp_id:
            description:
                - The MSP ID for the organization.
            type: str
            sample: Org1MSP
        root_certs:
            description:
                - The list of root certificates for this organization.
                - Root certificates must be supplied as base64 encoded PEM files.
            type: list
            elements: str
            sample: LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0t...
        intermediate_certs:
            description:
                - The list of intermediate certificates for this organization.
                - Intermediate certificates must be supplied as base64 encoded PEM files.
            type: list
            elements: str
            sample: LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0t...
        admins:
            description:
                - The list of administrator certificates for this organization.
                - Administrator certificates must be supplied as base64 encoded PEM files.
            type: list
            elements: str
            sample: LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0t...
        revocation_list:
            description:
                - The list of revoked certificates for this organization.
                - Revoked certificates must be supplied as base64 encoded PEM files.
            type: list
            elements: str
            sample: LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0t...
        tls_root_certs:
            description:
                - The list of TLS root certificates for this organization.
                - TLS root certificates must be supplied as base64 encoded PEM files.
            type: list
            elements: str
            sample: LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0t...
        tls_intermediate_certs:
            description:
                - The list of TLS root certificates for this organization.
                - TLS intermediate certificates must be supplied as base64 encoded PEM files.
            type: list
            elements: str
            sample: LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0t...
        fabric_node_ous:
            description:
                - Configuration specific to the identity classification.
            type: dict
            contains:
                enable:
                    description:
                        - True if identity classification is enabled for this organization, false otherwise.
                    type: boolean
                    sample: true
                admin_ou_identifier:
                    description:
                        - Configuration specific to the admin identity classification.
                    type: dict
                    contains:
                        certificate:
                            description:
                                - The root or intermediate certificate for this identity classification.
                                - Root or intermediate certificates must be supplied as base64 encoded PEM files.
                            type: str
                            sample: LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0t...
                        organizational_unit_identifier:
                            description:
                                - The organizational unit (OU) identifier for this identity classification.
                            type: str
                            sample: admin
                client_ou_identifier:
                    description:
                        - Configuration specific to the client identity classification.
                    type: dict
                    contains:
                        certificate:
                            description:
                                - The root or intermediate certificate for this identity classification.
                                - Root or intermediate certificates must be supplied as base64 encoded PEM files.
                            type: str
                            sample: LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0t...
                        organizational_unit_identifier:
                            description:
                                - The organizational unit (OU) identifier for this identity classification.
                            type: str
                            sample: client
                peer_ou_identifier:
                    description:
                        - Configuration specific to the peer identity classification.
                    type: dict
                    contains:
                        certificate:
                            description:
                                - The root or intermediate certificate for this identity classification.
                                - Root or intermediate certificates must be supplied as base64 encoded PEM files.
                            type: str
                            sample: LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0t...
                        organizational_unit_identifier:
                            description:
                                - The organizational unit (OU) identifier for this identity classification.
                            type: str
                            sample: peer
                orderer_ou_identifier:
                    description:
                        - Configuration specific to the orderer identity classification.
                    type: dict
                    contains:
                        certificate:
                            description:
                                - The root or intermediate certificate for this identity classification.
                                - Root or intermediate certificates must be supplied as base64 encoded PEM files.
                            type: str
                            sample: LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0t...
                        organizational_unit_identifier:
                            description:
                                - The organizational unit (OU) identifier for this identity classification.
                            type: str
                            sample: orderer
        organizational_unit_identifiers:
            description:
                - The list of organizational unit identifiers for this organization.
            type: list
            elements: dict
            contains:
                certificate:
                    description:
                        - The root or intermediate certificate for this organizational unit identifier.
                        - Root or intermediate certificates must be supplied as base64 encoded PEM files.
                    type: str
                    sample: LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0t...
                organizational_unit_identifier:
                    description:
                        - The organizational unit (OU) identifier.
                    type: str
                    sample: acctdept
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
        wait_timeout=dict(type='int', default=60)
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
        organization_list = get_all_organizations(console)

        organizations = list()

        for organization in organization_list:
            organizations.append(organization.to_json())

        # Return certificate authority information.
        module.exit_json(exists=True, organizations=organizations)

    # Notify Ansible of the exception.
    except Exception as e:
        module.fail_json(msg=to_native(e))


if __name__ == '__main__':
    main()
