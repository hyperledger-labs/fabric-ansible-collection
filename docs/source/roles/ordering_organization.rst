..
.. SPDX-License-Identifier: Apache-2.0
..

:github_url: https://github.com/hyperledger-labs/fabric-ansible-collection/edit/main/docs/source/roles/ordering_organization.rst


ordering_organization -- Build Hyperledger Fabric components for an ordering organization
===========================================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

This role allows you to quickly build Hyperledger Fabric components for an ordering organization. An ordering organization has a certificate authority and an ordering service.

This role works with the IBM Support for Hyperledger Fabric software or the Hyperledger Fabric Open Source Stack running in a Red Hat OpenShift or Kubernetes cluster.

Parameters
----------

  api_endpoint (required)
    The URL for the Fabric operations console.

    | **Type**: str

  api_authtype (required)
    ``ibmcloud`` - Authenticate to the Fabric operations console using IBM Cloud authentication. You must provide a valid API key using *api_key*.

    ``basic`` - Authenticate to the Fabric operations console using basic authentication. You must provide both a valid API key using *api_key* and API secret using *api_secret*.

    | **Type**: str

  api_key (required)
    The API key for the Fabric operations console.

    | **Type**: str

  api_secret
    The API secret for the Fabric operations console.

    Only required when *api_authtype* is ``basic``.

    | **Type**: str

  api_timeout
    The timeout, in seconds, to use when interacting with the Fabric operations console.

    | **Type**: int
    | **Default value**: ``60``

  state
    ``absent`` - All components for the ordering organization will be stopped and removed, if they exist.

    ``present`` - All components for the ordering organization will be created if they do not exist, or will be updated if their current configuration does not match the expected configuration.

    | **Type**: str
    | **Default value**: ``present``

  organization_name (required)
    The name of the ordering organization.

    | **Type**: str

  organization_msp_id (required)
    The MSP ID of the ordering organization.

    | **Type**: str

  ca_admin_enrollment_id (required)
    The enrollment ID, or user name, of the identity registered as the administrator of the certificate authority.

    | **Type**: str

  ca_admin_enrollment_secret (required)
    The enrollment secret, or password, of the identity registered as the administrator of the certificate authority.

    | **Type**: str

  ca_name
    The name of the certificate authority.

    By default, the certificate authority name is *organization_name* followed by `CA`, for example ``Org1 CA``.

    | **Type**: str

  ca_resources
    The Kubernetes resource configuration for the certificate authority.

    For more information, review the documentation for the *resources* parameter of the *certificate_authority* module: `certificate_authority <../modules/certificate_authority.html>`_

    | **Type**: dict

  ca_storage
    The Kubernetes storage configuration for the certificate authority.

    For more information, review the documentation for the *storage* parameter of the *certificate_authority* module: `certificate_authority <../modules/certificate_authority.html>`_

    | **Type**: dict

  ca_version
    The version of Hyperledger Fabric to use for the certificate authority.

    If you do not specify a version, the default Hyperledger Fabric version will be used for a new certificate authority.

    If you do not specify a version, an existing certificate authority will not be upgraded.

    If you specify a new version, an existing certificate authority will be automatically upgraded.

    | **Type**: str

  ca_zone
    The Kubernetes zone for this certificate authority.

    If you do not specify a Kubernetes zone, and multiple Kubernetes zones are available, then a random Kubernetes zone will be selected for you.

    | **Type**: str

  organization_admin_enrollment_id (required)
    The enrollment ID, or user name, of the identity registered as the administrator of the organization.

    | **Type**: str

  organization_admin_enrollment_secret (required)
    The enrollment secret, or password, of the identity registered as the administrator of the organization.

    | **Type**: str

  ordering_service_enrollment_id (required)
    The enrollment ID, or user name, of the identity registered for the ordering service.

    | **Type**: str

  ordering_service_enrollment_secret (required)
    The enrollment secret, or password, of the identity registered for the ordering service.

    | **Type**: str

  ordering_service_name
    The name of the ordering service.

    | **Type**: str
    | **Default value**: ``Ordering Service``

  ordering_service_nodes
    The number of ordering service nodes in the ordering service.

    For development and test networks, use one ordering service node. Five ordering service nodes provides Raft crash fault tolerance, and is suitable for production networks.

    | **Type**: int
    | **Default value**: ``1``

  ordering_service_resources
    The Kubernetes resource configuration for the ordering service.

    For more information, review the documentation for the *resources* parameter of the *ordering_service* module: `ordering_service <../modules/ordering_service.html>`_

    | **Type**: dict

  ordering_service_storage
    The Kubernetes storage configuration for the ordering service.

    For more information, review the documentation for the *storage* parameter of the *ordering_service* module: `ordering_service <../modules/ordering_service.html>`_

    | **Type**: dict

  ordering_service_version
    The version of Hyperledger Fabric to use for the ordering service.

    If you do not specify a version, the default Hyperledger Fabric version will be used for a new ordering service.

    If you do not specify a version, an existing ordering service will not be upgraded.

    If you specify a new version, an existing ordering service will be automatically upgraded.

    | **Type**: str

  ordering_service_zones
    The Kubernetes zones for this ordering service.

    If specified, you must provide a Kubernetes zone for each ordering service node in the ordering service.

    If you do not specify a Kubernetes zone, and multiple Kubernetes zones are available, then a random Kubernetes zone will be selected for you.

    | **Type**: list
    | **Elements**: str

  wallet
    The wallet directory to store identity files in.

    If you do not specify a wallet directory, then the wallet directory will be set to the directory containing the Ansible playbook being executed.

    | **Type**: str

  ca_admin_identity
    The identity file for the administrator of the certificate authority.

    By default, the identity file stored in the *wallet* directory, and the file is named *organization_name* followed by `CA Admin.json`, for example ``/path/to/my/wallet/Org1 CA Admin.json``.

  organization_admin_identity
    The identity file for the administrator of the organization.

    By default, the identity file stored in the *wallet* directory, and the file is named *organization_name* followed by ` Admin.json`, for example ``/path/to/my/wallet/Org1 Admin.json``.

  wait_timeout
    The timeout, in seconds, to wait until the certificate authority and the ordering service is available.

    | **Type**: int
    | **Default value**: ``60``

Examples
--------

.. code-block:: yaml+jinja

  - name: Create components for an ordering organization
    vars:
      state: present
      api_endpoint: https://fabric-console.example.org:32000
      api_authtype: basic
      api_key: xxxxxxxx
      api_secret: xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
      organization_name: Ordering Org
      organization_msp_id: OrdererMSP
      ca_admin_enrollment_id: admin
      ca_admin_enrollment_secret: adminpw
      organization_admin_enrollment_id: orderingorgadmin
      organization_admin_enrollment_secret: orderingorgadminpw
      ordering_service_enrollment_id: orderingorgorderer
      ordering_service_enrollment_secret: orderingorgordererpw
      wait_timeout: 3600
    roles:
      - hyperledger.fabric_ansible_collection.ordering_organization

  - name: Destroy components for an ordering organization
    vars:
      state: absent
      api_endpoint: https://fabric-console.example.org:32000
      api_authtype: basic
      api_key: xxxxxxxx
      api_secret: xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
      organization_name: Ordering Org
      wait_timeout: 3600
    roles:
      - hyperledger.fabric_ansible_collection.ordering_organization
