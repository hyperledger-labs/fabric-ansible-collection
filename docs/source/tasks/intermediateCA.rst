..
.. SPDX-License-Identifier: Apache-2.0
..

Creating an Intermediate Certificate Authority
=================================================

Hyperledger Fabric allows for the optional use of Intermediate CAs which can protect a root CA and provide operational flexibility. More information can be found in the Hyperledger Fabric documentation: https://hyperledger-fabric.readthedocs.io/en/release-2.5/identity/identity.html#root-cas-intermediate-cas-and-chains-of-trust.

The scenario in this task guide is that Magneto Corp wishes to create a Root CA for the corporation, and an Intermediate CA for a UK subsidiary.

The playbook has the following steps:
* Check for the presence of the Parent CA and exit if it already exists
* Create the Parent CA
* Register and enroll the identities for the Intermediate CA
* Check for the presence of the Intermediate CA and exit if it already exists
* Create the Intermediate CA

Before you start
----------------

This task guide assumes that you have installed Ansible and the Hyperledger Fabric Ansible Collection, and are familiar with how to use these technologies.

Cloning the repository
----------------------

This task guide uses an example playbook which is stored in a GitHub repository. You must clone this GitHub repository in order to run the playbook locally:

    .. highlight:: none

    ::

        git clone https://github.com/hyperledger-labs/fabric-ansible-collection.git

After cloning the GitHub repository, you must change into the examples directory for this task guide:

    ::

        cd fabric-ansible-collection/examples/create-intermediate-ca

Editing the variable file
-------------------------

You need to edit the variable file ``vars.yml``. This file is used to pass information about your network into the example Ansible playbook.

The first set of values that you must set are :

  1. Determine the URL of your instance's console.
  2. Determine the API key and secret you use to access your instance's console. You can also use a username and password instead of an API key and secret.
  3. Set ``api_endpoint`` to the URL of your console.
  4. Set ``api_authtype`` to ``basic``.
  5. Set ``api_key`` to your API key or username.
  6. Set ``api_secret`` to your API secret or password.

The remaining values must always be set:

* Set ``parent_ca_name:`` to the name of the parent CA, for example ``MGCorp``.
* Set ``parent_ca_admin_identity`` to the name of the Parent CA administrator enroll ID.
* Set ``parent_ca_admin_secret`` to the Parent CA administrator enroll secret.
* Set ``int_ca_identity`` to the name if the intermediate CA identity. (The identity will be created as type ``client`` and with the attribute ``hf.IntermediateCA``.)
* Set ``int_ca_secret`` to the secret of the intermediate CA identity.
* Set ``int_tlsca_identity`` to the name if the intermediate CA tls identity. (The identity will be created as type ``client`` and with the attribute ``hf.IntermediateCA``.)
* Set ``int_tlsca_secret`` to the secret of the intermediate CA tls identity.
* Set ``int_ca_name`` to the name of the intermediate CA, for example ``MGCUK``.
* Set ``int_ca_admin_identity`` to the name of the Intermediate CA administrator enroll ID.
* Set ``int_ca_admin_secret`` to the secret of the Intermediate CA administrator.
* Set ``int_tlsca_admin_identity`` to the name of the Intermediate CA tls administrator enroll ID.
* Set ``int_tlsca_admin_secret`` to the secret of the Intermediate CA tls administrator.


Creating the Parent CA and the Intermediate CA
----------------------------------------------

Review the example playbook `create-parent-plus-intermediate-ca.yml <https://github.com/hyperledger-labs/fabric-ansible-collection/blob/master/examples/create-intermediate-ca/create-parent-plus-intermediate-ca.yml>`_, then run it as follows:

  ::

    ansible-playbook create-parent-plus-intermediate-ca.yml

Ensure that the example playbook completed successfully by examining the ``PLAY RECAP`` section in the output from Ansible.

