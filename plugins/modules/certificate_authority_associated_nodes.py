#!/usr/bin/python
#
# SPDX-License-Identifier: Apache-2.0
#

from __future__ import absolute_import, division, print_function
__metaclass__ = type

from ..module_utils.module import BlockchainModule
from ..module_utils.utils import get_console, get_certs_from_certificate_authority, get_all_peers, get_all_orderering_service_nodes

from ansible.module_utils._text import to_native

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = '''
---
module: certificate_authority_info
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
    certificate_authority:
        description:
            - The name of the certificate authority.
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
  hyperledger.fabric_ansible_collection.certificate_authority_info:
    api_endpoint: https://console.example.org:32000
    api_authtype: basic
    api_key: xxxxxxxx
    api_secret: xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    name: Org1 CA
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
        certificate_authority=dict(type='raw'),
        registrar=dict(type='raw'),
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

        # Get any certificates from the certificate authority
        certificate_authority_certs = get_certs_from_certificate_authority(console, module)

        ca_tls_root_certs = certificate_authority_certs['tls_root_certs']

        # Get all of the peers
        peers_list = get_all_peers(console)

        peers = list()
        if peers_list is not None:
            for peer in peers_list:

                peer_root_certs = peer.to_json()['msp']['tlsca']['root_certs']

                intersection_list = list(set(ca_tls_root_certs) & set(peer_root_certs))

                # if the peer tls root cert intersects with the CA tls root certs, then add the peer
                if len(intersection_list) > 0:
                    peers.append(peer.to_json())

        # Get all of the ordering nodes
        ordering_service_nodes_list = get_all_orderering_service_nodes(console)

        ordering_service_nodes = list()
        if ordering_service_nodes_list is not None:
            for ordering_service_node in ordering_service_nodes_list:

                # Get the ordering node tls root certs
                ordering_service_node_root_certs = ordering_service_node.to_json()['msp']['tlsca']['root_certs']
                intersection_list = list(set(ca_tls_root_certs) & set(ordering_service_node_root_certs))

                # if the ordering node tls root cert intersects with the CA tls root certs, then add the ordering node
                if len(intersection_list) > 0:
                    ordering_service_nodes.append(ordering_service_node.to_json())

        # Return peer and orderering services nodes information.
        module.exit_json(exists=True, peers=peers, ordering_service_nodes=ordering_service_nodes)

    # Notify Ansible of the exception.
    except Exception as e:
        module.fail_json(msg=to_native(e))


if __name__ == '__main__':
    main()
