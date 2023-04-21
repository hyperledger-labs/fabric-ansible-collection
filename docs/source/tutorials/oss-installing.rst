..
.. SPDX-License-Identifier: Apache-2.0
..

Installing the Hyperledger Fabric Open Source Stack
===================================================

This tutorial will demonstrate how to use the Hyperledger Fabric Ansible Collection to automate the installation of the Hyperledger Fabric Open Source Stack into an IBM Cloud Kubernetes Service or Red Hat OpenShift cluster.

Once you have created an instance, follow the `Building a network <./building.html>`_ tutorial.

This tutorial uses the Ansible Fabric `fabric-operator-crds role <../roles/fabric-operator-crds.html>`_ and `fabric-console role <../roles/fabric-console.html>`_ to install the Hyperledger Fabric Open Source Operator and Console. If you wish to customize the installation process, then you should review the documentation for these roles.

Before you start
----------------

Ensure that you have installed all of the prerequisite software described in `Installation <../installation.html>`_.

You must have access to a Kubernetes Service or Red Hat OpenShift cluster that is supported for use with Hyperledger Fabric Open Source Stack. To get an idea of the supported platforms and resource requirements, you can reference the IBM Hyperledger Fabric Support Offering documentation: https://www.ibm.com/docs/en/hlf-support/1.0.0?topic=kubernetes-deploying-support-hyperledger-fabric

If you have a Kubernetes cluster, you must have the Kubernetes CLI (``kubectl``) installed and configured to use your Kubernetes cluster. Verify that it is working by running the following command:

::

    kubectl get nodes

If you have a Red Hat OpenShift cluster, you must have the Red Hat OpenShift CLI (``oc``) installed and configured to use your Red Hat OpenShift cluster. Verify that it is working by running the following command:

::

    oc get nodes

The Hyperledger Fabric Open Source Stack software should be installed into one Kubernetes namespace or Red Hat OpenShift project.

This namespace or project will contain the Hyperledger Fabric Open Source Stack Webhook and Custom Resource Definitions. This namespace or project will also contain the Hyperledger Fabric Open Source Operator and Console. It is recommended that you call this namespace or project ``oss-hlf-infra``.

The Ansible collection will attempt to automatically create the namespace or project for you. If you do not have permissions to create a namespace or project, then ask your administrator to create them for you.


Creating the playbook
---------------------

Create a new Ansible playbook file called `install-oss-hlf.yml`. Copy and paste the appropriate code block below, depending on the type of cluster that you are using:

**Kubernetes**

.. highlight:: yaml

::

    ---
    - name: Deploy Hyperledger Fabric Open Source Operator and Custom Resource Definitions
      hosts: localhost
      vars:
        state: present
        target: k8s
        arch: amd64
        namespace: oss-hlf-infra
        wait_timeout: 3600
      roles:
        - hyperledger.fabric-ansible-collection.fabric_operator_crds

    - name: Deploy Hyperledger Fabric Open Source Console
      hosts: localhost
      vars:
        state: present
        target: k8s
        arch: amd64
        namespace: oss-hlf-infra
        console_name: <console_name>
        console_domain: <console_domain>
        console_email: <console_email>
        console_default_password: <console_default_password>
        console_storage_class: <console_storage_class>
        console_tls_secret: <console_tls_secret>
        wait_timeout: 3600
      roles:
        - hyperledger.fabric-ansible-collection.fabric_console

**Red Hat OpenShift**

.. highlight:: yaml

::

    ---
    - name: Deploy Hyperledger Fabric Open Source Operator and Custom Resource Definitions
      hosts: localhost
      vars:
        state: present
        target: openshift
        arch: amd64
        project: oss-hlf-infra
        wait_timeout: 3600
      roles:
        - hyperledger.fabric-ansible-collection.fabric_operator_crds

    - name: Deploy Hyperledger Fabric Open Source Console
      hosts: localhost
      vars:
        state: present
        target: openshift
        arch: amd64
        project: oss-hlf-infra
        console_domain: <console_domain>
        console_email: <console_email>
        console_default_password: <console_default_password>
        wait_timeout: 3600
      roles:
        - hyperledger.fabric-ansible-collection.fabric_console

Next, you will need to replace the variable placeholders with the required values.

Replace ``<console_name>`` with your custom name for your HLF Console.

Replace ``<console_domain>`` with the domain name of your Kubernetes cluster or Red Hat OpenShift cluster. This domain name is used as the base domain name for all ingress or routes created by the Hyperledger Fabric Open Source Stack.

Replace ``<console_email>`` with the email address of the Hyperledger Fabric Open Source Stack console user that will be created during the installation process. You will use this email address to access the Hyperledger Fabric Open Source Stack console after installation.

Replace ``<console_default_password>`` with the default password for the Hyperledger Fabric Open Source Stack console. This default password will be set as the password for all new users, including the user created during the installation process.

Replace ``<console_storage_class>`` with the Kubernetes or Red Hat Openshift StorageClass that must be used for all Hyperledger Fabric components.

Replace ``<console_tls_secret>`` with the Kubernetes or Red Hat Openshift secret to terminate TLS traffic. This secret must be present in the namespace before installing the Hyperledger Fabric Open Source Console.

By default, the ``<wait_timeout>`` variable is set to ``3600`` seconds (1 hour), which should be sufficient for most environments. You only need to change the value for this variable if you find that timeout errors occur during the installation process.

Running the playbook
--------------------

Run the Ansible playbook file you created in the previous step by running the following command:

    ::

        ansible-playbook install-oss-hlf.yml

The Ansible playbook will take some time to run. As the playbook runs, it will output information on the tasks being executed.

At the end of the output, you should see text similar to the following:

    .. highlight:: none

    ::

        TASK [console : Wait for console to start] ***********************************************************************
        ok: [localhost]

        TASK [console : Print console URL] *******************************************************************************
        ok: [localhost] => {
            "msg": "Hyperledger Fabric Open Source Stack console available at https://my-namespace-oss-hlf-console-console.apps.my-cluster.example.org"
        }

        TASK [console : Delete console] **********************************************************************************
        skipping: [localhost]

        PLAY RECAP *******************************************************************************************************
        localhost                  : ok=19   changed=4    unreachable=0    failed=0    skipped=13   rescued=0    ignored=0

Ensure that no errors are reported in the output. Ensure that the failure count in the final ``PLAY RECAP`` section is 0.

The URL of the Hyperledger Fabric Open Source Console is displayed as part of the output for the ``Print console URL`` task. When you access this URL, you can log in with the email and default password that you specified in your Ansible playbook.

You have now finished installing the Hyperledger Fabric Open Source Stack software.
