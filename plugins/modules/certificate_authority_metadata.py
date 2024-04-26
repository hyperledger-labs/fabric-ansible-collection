#!/usr/bin/python
#
# SPDX-License-Identifier: Apache-2.0
#

from __future__ import absolute_import, division, print_function
__metaclass__ = type

from ..module_utils.module import BlockchainModule
from ..module_utils.certificate_authorities import CertificateAuthority
from ..module_utils.utils import get_console
from ..module_utils.url_utils import translate_url_to_os_format

from ansible.module_utils._text import to_native

import json

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = '''
---
module: certificate_authority_metadata
short_description: Update information about a Hyperledger Fabric certificate authority metadata
description:
    - Updates metadata for a certificate authority.
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
    name:
        description:
            - The name of the certificate authority.
        required: true
    preferred_url:
        description:
            - Preferred URL style for the components.
            - os is used the open source style with standard ports (443)
            - legacy is the software as a service style URLs
        required: false
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
    preferred_url: os
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
        preferred_url=dict(type='str', choices=['os', 'legacy']),
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

        changed = False

        # Determine if the certificate authority exists.
        certificate_authority = console.get_component_by_display_name('fabric-ca', module.params['name'], deployment_attrs='included')

        # If it doesn't exist, return now.
        if certificate_authority is None:
            return module.exit_json(exists=False)

        if module.params['preferred_url'] is None:
            return module.exit_json(exists=False)

        if certificate_authority['imported'] == False:

            certificate_authority_metadata_update = dict(
                preferred_url=module.params['preferred_url']
            )

        else:

            certificate_authority_metadata_update = dict(
                api_url = translate_url_to_os_format(certificate_authority['api_url'], 'ca'),
                operations_url = translate_url_to_os_format(certificate_authority['operations_url'], 'operations')
            )

        certificate_authority = console.update_metadata_ca(certificate_authority['id'], certificate_authority_metadata_update)
        changed = True

        certificate_authority = CertificateAuthority.from_json(console.extract_ca_info(certificate_authority))
        timeout = module.params['wait_timeout']
        certificate_authority.wait_for(timeout)

        # Return certificate authority information.
        module.exit_json(changed=changed, certificate_authority=certificate_authority.to_json())

    # Notify Ansible of the exception.
    except Exception as e:
        module.fail_json(msg=to_native(e))


if __name__ == '__main__':
    main()
