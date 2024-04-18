#!/usr/bin/python
#
# SPDX-License-Identifier: Apache-2.0
#

from __future__ import absolute_import, division, print_function
__metaclass__ = type

from ..module_utils.module import BlockchainModule
from ..module_utils.utils import get_console, get_all_organizations, resolve_identity
from ..module_utils.msp_utils import convert_identity_to_msp_path
from ..module_utils.enrolled_identities import EnrolledIdentity

from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.backends import default_backend

from pathlib import Path
import json
import os
import base64
import datetime
import tempfile
import shutil
import subprocess

from ansible.module_utils._text import to_native

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = '''
---
module: membership_service_provider_local
short_description: Construct a set of membership service provider directories
description:
    - Gather information about all organizations
    - Create a directory for each organization named by the msp_id.
    - Create an msp folder for each msp to store the identity
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
    operation:
        description:
            - C(create) - Create an organizations directory with the MSPs for all organizations
        type: str
        required: true
    organization_dir:
        description:
            - Directory used for creating local MSPs for all organizations.
            - Default is organizations.
        type: str
    wallet:
        description:
            - Directory used for storing the admin certficates from the console wallet.
            - Default is wallet.
        type: str
    wait_timeout:
        description:
            - The timeout, in seconds, to wait until the certificate authority is available.
        type: int
        default: 60
notes: []
requirements: []
'''

EXAMPLES = '''
- name: Create the local msp for all organizations
  hyperledger.fabric_ansible_collection.membership_service_provider_local:
    api_endpoint: https://console.example.org:32000
    api_authtype: basic
    api_key: xxxxxxxx
    api_secret: xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    operation: "create"
'''

RETURN = '''
---
exists:
    description:
        - True if the process succeeds and creates the organizations directory.
    returned: always
    type: boolean
'''


def create(module):

    # Ensure all exceptions are caught.
    try:

        # timeout = module.params['wait_timeout']

        organizations_dir = module.params['organizations_dir']

        if os.path.exists(organizations_dir):
            shutil.rmtree(organizations_dir)

        wallet_dir = module.params['wallet_dir']

        # Log in to the console.
        console = get_console(module)

        organization_list = get_all_organizations(console)

        for organization in organization_list:

            Path(os.path.join(organizations_dir, organization.msp_id, 'msp')).mkdir(parents=True, exist_ok=True)

            with open(os.path.join(organizations_dir, organization.msp_id, organization.msp_id + '.json'), 'w', encoding='utf-8') as f:
                json.dump(organization.to_json(), f, ensure_ascii=False, indent=4)

            # Scan the entries in the wallet directory
            file_names = [fn for fn in os.listdir(wallet_dir) if fn.endswith('json')]
            for identity_filename in file_names:

                identity_filename_path = os.path.join(wallet_dir, identity_filename)

                # Open the json for the identity
                with open(identity_filename_path, 'r') as file:
                    identity = json.load(file)

                # decode the certificate
                cert = x509.load_pem_x509_certificate(base64.b64decode(identity['cert']), default_backend())

                # extract the nodeOU
                ou = cert.subject.get_attributes_for_oid(NameOID.ORGANIZATIONAL_UNIT_NAME)[0].value

                if 'admin' not in ou:
                    module.json_log({
                        'msg': f'{identity_filename_path} is not an admin cert'
                    })
                    continue

                if cert.not_valid_after < datetime.datetime.now():
                    module.json_log({
                        'msg': f'{identity_filename_path} has expired'
                    })
                    continue

                identity_found = False

                # if this cert matches the admin cert in the msp, then create the local msp and move to the next cert
                for admin_cert in organization.admins:
                    if identity['cert'] == admin_cert:
                        create_local_msp(console, module, identity_filename_path, organizations_dir, identity, organization.msp_id)
                        identity_found = True
                        break

                if identity_found:
                    break

                try:

                    # Create a temporary directory.
                    cert_path = tempfile.mkdtemp()

                    certificate_file = os.path.join(cert_path, 'cert.pem')

                    write_cert_to_file(certificate_file, identity['cert'])

                    identity_found = False
                    for root_cert in organization.root_certs:

                        ca_certificate_file = os.path.join(cert_path, 'cacert.pem')
                        write_cert_to_file(ca_certificate_file, root_cert)

                        result = subprocess.run(['openssl', 'verify', '-CAfile', ca_certificate_file, certificate_file], capture_output=True, text=True)

                        if result.returncode == 0:
                            create_local_msp(console, module, identity_filename, organizations_dir, identity, organization.msp_id)
                            identity_found = True
                            break

                    if identity_found:
                        break

                finally:
                    shutil.rmtree(cert_path)

        module.exit_json(changed=True)

    # Notify Ansible of the exception.
    except Exception as e:
        module.fail_json(msg=to_native(e))


def write_cert_to_file(filename, cert):
    f = open(filename, "w")
    f.write(base64.b64decode(cert).decode("ascii"))
    f.close()


def create_local_msp(console, module, identity_filename_path, organizations_dir, identity, msp_id):
    shutil.copyfile(identity_filename_path, os.path.join(organizations_dir, msp_id, 'identity.json'))
    enrolled_identity = EnrolledIdentity.from_json(identity)
    resolved_identity = resolve_identity(console, module, enrolled_identity, msp_id)
    convert_identity_to_msp_path(resolved_identity, os.path.join(organizations_dir, msp_id, 'msp'))


def main():

    # Create the module.
    argument_spec = dict(
        api_endpoint=dict(type='str', required=True),
        api_authtype=dict(type='str', required=True, choices=['ibmcloud', 'basic']),
        api_key=dict(type='str', required=True, no_log=True),
        api_secret=dict(type='str', no_log=True),
        api_timeout=dict(type='int', default=60),
        api_token_endpoint=dict(type='str', default='https://iam.cloud.ibm.com/identity/token'),
        operation=dict(type='str', required=True, choices=['create']),
        organizations_dir=dict(type='str', default='organizations'),
<<<<<<< HEAD
        wallet_dir=dict(type='str', default='wallet'),
=======
        wallet=dict(type='str', default='wallet'),
>>>>>>> 53dd49d (Add support for local MSP, channel config)
        wait_timeout=dict(type='int', default=60)
    )
    required_if = [
        ('api_authtype', 'basic', ['api_secret'])
    ]
    module = BlockchainModule(argument_spec=argument_spec, supports_check_mode=True, required_if=required_if)

    # Ensure all exceptions are caught.
    try:
        operation = module.params['operation']
        if operation == 'create':
            create(module)
        else:
            raise Exception(f'Invalid operation {operation}')

    # Notify Ansible of the exception.
    except Exception as e:
        module.fail_json(msg=to_native(e))


if __name__ == '__main__':
    main()
