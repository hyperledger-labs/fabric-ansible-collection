..
.. SPDX-License-Identifier: Apache-2.0
..

Certificate Management
======================

This article will show you how to enroll/re-enroll/renew the following certificates: CA TLS certificate, Peer TLS/Ecert, and Orderer TLS/Ecert certificates on an existing Hyperledger Fabric network.

For this tutorial, you can use the IBM Support for Hyperledger Fabric software running in a Red Hat OpenShift or Kubernetes cluster.

Note: If the Orderer TLS certificate expired. We will not able renew the certificate using this process.

Before you start
----------------
You will need to use the GitHub repositorythat you cloned in the previous tutorial. Ensure that you are in the tutorial directory:

    ::

        cd ansible-collection/tutorial

Peer/Orderer Ecert/TLS certificate Enroll/Re-enroll
===================================================

For re-enroll/enroll the Peer TLS/Ecert you have edit the playbook `24-reenroll-peer-tls-and-ecert.yml` and change respective `vars_files` that you want re-enroll/enroll peer certificates. Once you have edited the file. Please execute the below command for the certificate renewal.

    ::

        ./enroll_or_reenroll_peer_and_orderer_cert.sh [-i] [-i <component type>] [-j <certificate type>] [-k <action>]

Next, you will need to replace the variable placeholders with the required values.

Replace ``<component type>`` with your component type for your HLF Console like `peer` or `orderer`.

Replace ``<certificate type>`` with the certificate type that you want enroll/re-enroll like `ecert` OR `tls_cert`.

Replace ``<action>`` with the action that you want to take enroll/re-enroll like `enroll` OR `reenroll` OR `restart`.


Once you have replaced the above variable in the command. Execute the command,It will update and restart the peer. If the peer restarted successfully, please refresh the certs in the console of the corresponding component.


CA TLS certificate Renewal
==========================

We will examine the process for renewing the CA TLS certificate in this section. We offer two options here: either renew the specific CA TLS certificate or renew all CA TLS certificates in the instance.

For renewing all the CA components in the instance you have to edit the playbook `26-renew-all-ca-tls.yml` and change respective components `vars_files` that you want renew CA TLS certificates. Once you have edited the file. Please execute the below command for the certificate renewal.

  ::

        ./renew_ca_tls_cert.sh [-k <action flag>]


Next, you will need to replace the variable placeholders with the required values.

Replace ``<component name>`` with name of your CA component.

Replace ``<component type>`` with the component type like 'peer' or 'orderer'. We use this flag to associate respective node with the CA.

Replace ``<action flag>``  we are using the flag for renewing all the CA TLS certificates in instance. The flag will be like `all`.


For renewing respective CA component in the instance you have to edit the playbook `30-renew-ca-tls.yml` and change respective components `vars_files` that you want renew CA TLS certificates. Once you have edited the file. Please execute the below command for the certificate renewal.


    ::

         ./renew_ca_tls_cert.sh [-i <component name>] [-j <component type>]

Next, you will need to replace the variable placeholders with the required values.

Replace ``<component name>`` with name of your CA component.

Replace ``<component type>`` with the component type like 'peer' or 'orderer'. We use this flag to associate respective node with the CA..

Once you've changed the above variable in the command. When you run the command, the CA will be updated and restarted, as well as the nodes associated with it. Once the process is finished, please refresh the certs in the appropriate CA component in console.
