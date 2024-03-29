#!/usr/bin/python
#
# SPDX-License-Identifier: Apache-2.0
#

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import os
import shutil

from ansible.module_utils._text import to_native
from ansible.module_utils.basic import _load_params, env_fallback

from ..module_utils.file_utils import equal_files, get_temp_file
from ..module_utils.module import BlockchainModule
from ..module_utils.ordering_services import OrderingService
from ..module_utils.utils import (get_console, get_identity_by_module,
                                  get_ordering_service_by_module,
                                  get_ordering_service_nodes_by_module,
                                  resolve_identity)

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = '''
---
module: channel_block
short_description: Fetch blocks for a Hyperledger Fabric channel
description:
    - Fetch blocks for a Hyperledger Fabric channel.
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
            - C(absent) - If a block exists at the specified I(path), it will be removed.
            - C(present) - Fetch the block from the specified channel and store it at the specified I(path).
        type: str
        default: present
        choices:
            - absent
            - present
    ordering_service:
        description:
            - The ordering service to use to manage the channel.
            - You can pass a string, which is the cluster name of a ordering service registered
              with the Fabric operations console.
            - You can also pass a list, which must match the result format of one of the
              M(ordering_service_info) or M(ordering_service) modules.
            - Only required when I(operation) is C(fetch).
            - Cannot be specified with I(ordering_service_nodes).
        type: raw
        required: true
    ordering_service_nodes:
        description:
            - The ordering service nodes to use to manage the channel.
            - You can pass strings, which are the names of ordering service nodes that are
              registered with the Fabric operations console.
            - You can also pass a dict, which must match the result format of one
              of the M(ordering_service_node_info) or M(ordering_service_node) modules.
            - Only required when I(operation) is C(fetch).
            - Cannot be specified with I(ordering_service).
        type: raw
    identity:
        description:
            - The identity to use when interacting with the ordering service or for signing
              channel configuration update transactions.
            - You can pass a string, which is the path to the JSON file where the enrolled
              identity is stored.
            - You can also pass a dict, which must match the result format of one of the
              M(enrolled_identity_info) or M(enrolled_identity) modules.
        type: raw
        required: true
    msp_id:
        description:
            - The MSP ID to use for interacting with the ordering service or for signing
              channel configuration update transactions.
        type: str
        required: true
    hsm:
        description:
            - "The PKCS #11 compliant HSM configuration to use for digital signatures."
            - Only required if the identity specified in I(identity) was enrolled using an HSM.
        type: dict
        suboptions:
            pkcs11library:
                description:
                    - "The PKCS #11 library that should be used for digital signatures."
                type: str
            label:
                description:
                    - The HSM label that should be used for digital signatures.
                type: str
            pin:
                description:
                    - The HSM pin that should be used for digital signatures.
                type: str
    name:
        description:
            - The name of the channel.
        type: str
        required: true
    target:
        description:
            - The target block to fetch.
            - Can be the number of the block to fetch, or one of C(newest), C(oldest) or C(config).
        type: str
        required: true
    path:
        description:
            - The path to the file where the channel configuration or the channel configuration
              update transaction will be stored.
        type: str
        required: true
    tls_handshake_time_shift:
        type: str
        description:
            - The amount of time to shift backwards for certificate expiration checks during TLS handshakes with the ordering service endpoint.
            - Only use this option if the ordering service TLS certificates have expired.
            - The value must be a duration, for example I(30m), I(24h), or I(6h30m).
notes: []
requirements: []
'''

EXAMPLES = '''
- name: Fetch the genesis block for the channel
  hyperledger.fabric_ansible_collection.channel_block:
    state: present
    api_endpoint: https://console.example.org:32000
    api_authtype: basic
    api_key: xxxxxxxx
    api_secret: xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    ordering_service: Ordering Service
    identity: Org1 Admin.json
    msp_id: Org1MSP
    name: mychannel
    target: "0"
    path: channel_genesis_block.bin
'''

RETURN = '''
---
path:
    description:
        - The path to the file where the channel block is stored.
    type: str
    returned: always
'''


def main():

    # Create the module.
    argument_spec = dict(
        state=dict(type='str', default='present', choices=['present', 'absent']),
        api_endpoint=dict(type='str', required=True),
        api_authtype=dict(type='str', required=True, choices=['ibmcloud', 'basic']),
        api_key=dict(type='str', required=True, no_log=True),
        api_secret=dict(type='str', no_log=True),
        api_timeout=dict(type='int', default=60),
        api_token_endpoint=dict(type='str', default='https://iam.cloud.ibm.com/identity/token'),
        operation=dict(type='str', choices=['fetch']),
        ordering_service=dict(type='raw'),
        ordering_service_nodes=dict(type='list', elements='raw'),
        tls_handshake_time_shift=dict(type='str', fallback=(env_fallback, ['IBP_TLS_HANDSHAKE_TIME_SHIFT'])),   # TODO: Look into renaming this env variable
        identity=dict(type='raw'),
        msp_id=dict(type='str'),
        hsm=dict(type='dict', options=dict(
            pkcs11library=dict(type='str', required=True),
            label=dict(type='str', required=True, no_log=True),
            pin=dict(type='str', required=True, no_log=True)
        )),
        name=dict(type='str'),
        path=dict(type='str', required=True),
        target=dict(type='str')
    )
    required_if = [
        ('api_authtype', 'basic', ['api_secret']),
        ('state', 'present', ['identity', 'msp_id', 'name', 'target']),
    ]
    # Ansible doesn't allow us to say "require one of X and Y only if condition A is true",
    # so we need to handle this ourselves by seeing what was passed in.
    actual_params = _load_params()
    if actual_params.get('state', None) == 'present':
        required_one_of = [
            ['ordering_service', 'ordering_service_nodes']
        ]
    else:
        required_one_of = []
    module = BlockchainModule(argument_spec=argument_spec, supports_check_mode=True, required_if=required_if, required_one_of=required_one_of)

    # Validate HSM requirements if HSM is specified.
    if module.params['hsm']:
        module.check_for_missing_hsm_libs()

    # Ensure all exceptions are caught.
    try:

        # Log in to the console.
        console = get_console(module)

        # Handle the state is absent case first.
        state = module.params['state']
        path = module.params['path']
        path_exists = os.path.isfile(path)
        if state == 'absent' and path_exists:
            os.remove(path)
            return module.exit_json(changed=True)
        elif state == 'absent':
            return module.exit_json(changed=False)

        # Get the ordering service.
        ordering_service_specified = module.params['ordering_service'] is not None
        if ordering_service_specified:
            ordering_service = get_ordering_service_by_module(console, module)
        else:
            ordering_service_nodes = get_ordering_service_nodes_by_module(console, module)
            ordering_service = OrderingService(ordering_service_nodes)
        tls_handshake_time_shift = module.params['tls_handshake_time_shift']

        # Get the identity.
        identity = get_identity_by_module(module)
        msp_id = module.params['msp_id']
        hsm = module.params['hsm']
        identity = resolve_identity(console, module, identity, msp_id)

        # Get the channel and target path.
        name = module.params['name']
        target = module.params['target']

        # Create a temporary file to hold the block.
        block_proto_path = get_temp_file()
        try:

            # Fetch the block.
            with ordering_service.connect(module, identity, msp_id, hsm, tls_handshake_time_shift) as connection:
                connection.fetch(name, target, block_proto_path)

            # Compare and copy if needed.
            if os.path.exists(path):
                changed = not equal_files(path, block_proto_path)
                if changed:
                    shutil.copyfile(block_proto_path, path)
                module.exit_json(changed=changed, path=path)
            else:
                shutil.copyfile(block_proto_path, path)
                module.exit_json(changed=True, path=path)

        # Ensure the temporary file is cleaned up.
        finally:
            os.remove(block_proto_path)

    # Notify Ansible of the exception.
    except Exception as e:
        module.fail_json(msg=to_native(e))


if __name__ == '__main__':
    main()
