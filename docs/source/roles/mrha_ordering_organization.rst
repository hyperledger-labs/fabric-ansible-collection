..
.. SPDX-License-Identifier: Apache-2.0
..

:github_url: https://github.com/IBM-Blockchain/ansible-collection/edit/main/docs/source/roles/mrha_ordering_organization.rst


mrha_ordering_organization -- Build Hyperledger Fabric components for a multi-region, highly available ordering organization
============================================================================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

This role allows you to quickly build Hyperledger Fabric components for a multi-region, highly available ordering organization. A multi-region, highly available ordering organization
has a certificate authority with multiple replicas and an ordering service with the ordering service nodes distributed across multiple regions.

This role works with the IBM Blockchain Platform managed service running in IBM Cloud, or the IBM Blockchain Platform software running in a Red Hat OpenShift or Kubernetes cluster.
You will need separate instances of the IBM Blockchain Platform for each region, as well as separate Red Hat OpenShift or Kubernetes clusters for each region.

Consult the IBM Blockchain Platform documentation for more information on high availability configurations: https://cloud.ibm.com/docs/blockchain?topic=blockchain-ibp-console-ha

Parameters
----------

  regions (required)
    The list of regions to use to build the components for a multi-region, highly available ordering organization.

    | **Type**: list
    | **Elements**: dict

    api_endpoint (required)
      The URL for the IBM Blockchain Platform console in this region.

      | **Type**: str

    api_authtype (required)
      ``ibmcloud`` - Authenticate to the IBM Blockchain Platform console in this region using IBM Cloud authentication. You must provide a valid API key using *api_key*.

      ``basic`` - Authenticate to the IBM Blockchain Platform console in this region using basic authentication. You must provide both a valid API key using *api_key* and API secret using *api_secret*.

      | **Type**: str

    api_key (required)
      The API key for the IBM Blockchain Platform console in this region.

      | **Type**: str

    api_secret
      The API secret for the IBM Blockchain Platform console in this region.

      Only required when *api_authtype* is ``basic``.

      | **Type**: str

    api_timeout
      The timeout, in seconds, to use when interacting with the IBM Blockchain Platform console in this region.

      | **Type**: int
      | **Default value**: ``60``

    api_token_endpoint
      The IBM Cloud IAM token endpoint to use when using IBM Cloud authentication in this region.

      Only required when *api_authtype* is ``ibmcloud``, and you are using IBM internal staging servers for testing.

      | **Type**: str
      | **Default value**: ``https://iam.cloud.ibm.com/identity/token``

    zones
      The list of zones, for example ``dal10``, ``dal12``, and ``dal13``, that the Red Hat OpenShift or Kubernetes cluster in this region has been configured with. The ordering service nodes created by this role will be distributed across these zones.

      | **Type**: list
      | **Elements**: str

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

  ca_db_type
    ``postgres`` - Use PostgreSQL for the certificate authority database. You must create the PostgreSQL instance that will be used by the certificate authority.

    | **Type**: str
    | **Default value**: ``postgres``

  ca_db_datasource (required)
    The datasource string for the certificate authority database connection.

    An example datasource string for PostgreSQL is: ``host=postgresql.example.org port=5432 user=myuser password=mypassword dbname=mydb sslmode=verify-full``

    For more information, review the Hyperledger Fabric documentation: https://hyperledger-fabric-ca.readthedocs.io/en/release-1.4/users-guide.html#configuring-the-database

    | **Type**: str

  ca_db_tls_enabled
    True if the certificate authority database uses TLS to secure network communications, false otherwise.

    | **Type**: bool
    | **Default value**: ``true``

  ca_db_tls_certfiles
    The list of TLS CA certificates required to verify the connection to the certificate authority database.

    TLS CA certificates must be supplied as base64 encoded PEM files.

    | **Type**: list
    | **Elements**: str

  ca_replicas
    The number of Kubernetes replicas to use for the certificate authority.

    | **Type**: int
    | **Default value**: ``3``

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

    | **Type**: int
    | **Default value**: ``5``

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

  - name: Create components for a multi-region, highly available ordering organization
    vars:
      state: present
      regions:
        - api_endpoint: https://ibp-console-dallas.example.org:32000
          api_authtype: basic
          api_key: xxxxxxxx
          api_secret: xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
        - api_endpoint: https://ibp-console-london.example.org:32000
          api_authtype: basic
          api_key: xxxxxxxx
          api_secret: xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
        - api_endpoint: https://ibp-console-tokyo.example.org:32000
          api_authtype: basic
          api_key: xxxxxxxx
          api_secret: xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
      organization_name: Ordering Org
      organization_msp_id: OrdererMSP
      ca_admin_enrollment_id: admin
      ca_admin_enrollment_secret: adminpw
      ca_db_datasource: host=postgresql.example.org port=5432 user=myuser password=mypassword dbname=mydb sslmode=verify-full
      ca_db_tls_certfiles:
        - LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0t...
      organization_admin_enrollment_id: orderingorgadmin
      organization_admin_enrollment_secret: orderingorgadminpw
      ordering_service_enrollment_id: orderingorgorderer
      ordering_service_enrollment_secret: orderingorgordererpw
      wait_timeout: 3600
    roles:
      - hyperledger.fabric-ansible-collection.mrha_ordering_organization

  - name: Destroy components for a multi-region, highly available ordering organization
    vars:
      state: absent
      regions:
        - api_endpoint: https://ibp-console-dallas.example.org:32000
          api_authtype: basic
          api_key: xxxxxxxx
          api_secret: xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
        - api_endpoint: https://ibp-console-london.example.org:32000
          api_authtype: basic
          api_key: xxxxxxxx
          api_secret: xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
        - api_endpoint: https://ibp-console-tokyo.example.org:32000
          api_authtype: basic
          api_key: xxxxxxxx
          api_secret: xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
      organization_name: Ordering Org
      wait_timeout: 3600
    roles:
      - hyperledger.fabric-ansible-collection.mrha_ordering_organization
