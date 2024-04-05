..
.. SPDX-License-Identifier: Apache-2.0
..

Certificate Management
======================

This tutorial will demonstrate how to enroll/re-enroll/renew the CA TLS certificate , Peer TLS/Ecert and Orderer TLS/Ecert certificates an existing Hyperledger Fabric network.

For this tutorial, you can use the IBM Support for Hyperledger Fabric software running in a Red Hat OpenShift or Kubernetes cluster.

Note: If the Orderer TLS certificate expired. We will not able renew the certificate using this process.

Before you start
----------------
You will need to use the GitHub repositorythat you cloned in the previous tutorial. Ensure that you are in the tutorial directory:

    .. highlight:: none

    ::

        cd ansible-collection/tutorial

Peer Enrollment/TLS certificate Management
==========================================

For re-enroll/enroll the Peer TLS/Ecert you hav edit the playbook `24-reenroll-peer-tls-and-ecert.yml` and change respective `vars_files` that you want re-enroll/enroll peer certificates. Once you have edited the file. Please execute the below command for the certificate renewal.

    ::

        ./enroll_or_reenroll_peer_and_orderer_cert [-i] [-i <Component Type>] [-j <Certificate Type>] [-k <action>]

