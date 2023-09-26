..
.. SPDX-License-Identifier: Apache-2.0
..

============
Installation
============

Requirements
------------

In order to use this Ansible collection, you must have the following pre-requisite software installed and available.

..
    TODO: Test the latest python version

Python v3.8
-----------

Python can be installed from a variety of sources, including the package manager for your operating system (apt, yum, etc).
If you install Python from the package manager for your operating system, you must also install the development libraries (usually a package named ``python3-devel``), as these are required when installing modules through ``pip``.

- The official Python website: https://www.python.org/downloads/
- The unofficial Python version manager: https://github.com/pyenv/pyenv

..
    TODO: Test the latest Ansible version

Ansible v2.9+
-------------

Ansible can be installed from a variety of sources, including the package manager for your operating system (apt, yum, etc). You can also install it using ``pip``, the package manager for Python:

::

    pip install -U 'ansible'

Hyperledger Fabric v2.4.7+ binaries
-----------------------------------

This Ansible collection requires use of the binaries from Hyperledger Fabric v2.4.7 or later to interact with the peers and ordering services in your Hyperledger Fabric networks. These binaries include ``configtxlator`` and ``peer``.

You can install these binaries by following the Hyperledger Fabric documentation: https://hyperledger-fabric.readthedocs.io/en/release-2.5/install.html

These binaries must be on the ``PATH`` of the system that will be used to run your Ansible Playbooks. You can check that the binaries are installed correctly by running:

::

    peer version

..
    TODO: Test with the latest (1.0.0) version of the python sdk

Hyperledger Fabric SDK for Python v0.8.1+
-----------------------------------------

This Ansible collection uses the Hyperledger Fabric SDK for Python to interact with the certificate authorities in your Hyperledger Fabric networks.

You can install this SDK using ``pip``, the package manager for Python:

::

    pip install -U fabric-sdk-py

PKCS #11/Cryptoki for Python v0.6.0+
------------------------------------

Optional: only required if you wish to store enrolled identities in a PKCS #11 compliant HSM.

You can install this SDK using ``pip``, the package manager for Python:

::

    pip install -U python-pkcs11

OpenShift client for Python v0.10.3+
------------------------------------

This Ansible collection uses the OpenShift client for Python to interact with your Red Hat OpenShift or Kubernetes cluster when installing the IBM Blockchain Platform software.

You can install this SDK using ``pip``, the package manager for Python:

::

    pip install -U 'openshift'

Semantic Versioning for Python v2.8.5+
--------------------------------------

This Ansible collection uses Semantic Versioning for Python to handle version ranges when determining which version of Hyperledger Fabric to use.

You can install this SDK using using ``pip``, the package manager for Python:

::

    pip install -U semantic_version


Hyperledger Fabric OSS vX.Y.Z or IBM HLF Support v1.0.0
--------------------------------------------------------

This Ansible collection is mainly to be used to manage network components and therefore requires the Hyperledger Fabric Open Source Stack or the IBM Hyperledger Fabric Support Offering to be installed.

You can also use this Ansible collection to install either of these options. To see how to do this, follow either of the following tutorials:

1. `Installing the Hyperledger Fabric Open Source Stack <./tutorials/installing-fabric-operator-console.html>`_
2. `Installing the IBM Hyperledger Fabric Support Offering <./tutorials/hlfsupport-installing.html>`_


..
    TODO: Create a new Ansible Galaxy location to push the playbooks to and link the new URL

[COMING SOON] Installing using Ansible Galaxy
---------------------------------------------

Ansible Galaxy is the package manager for Ansible. The collection is published to Ansible Galaxy here: https://galaxy.ansible.com/COMING/SOON


You can use the ``ansible-galaxy`` command to install a collection from Ansible Galaxy, the package manager for Ansible:

::

    ansible-galaxy collection install COMING_SOON

Installing from source
----------------------

You may wish to install the collection from source if you cannot access Ansible Galaxy due to firewall or proxy issues, or if you need to install a version of the collection that has not yet been published.

You can use the ``ansible-galaxy`` command to install a collection built from source. To build your own collection, follow these steps:
This will build the stable `release-1.2` branch for v1.2.; use the `main` branch for the `2.0.0-beta` level

1. Clone the repository:

::

    git clone --branch main https://github.com/hyperledger-labs/fabric-ansible-collection.git

2. Build the collection artifact:

::

    cd ansible-collection
    ansible-galaxy collection build

3. Install the collection, replacing ``x.y.z`` with the current version:

::

    ansible-galaxy collection install fabric_ansible_collection-x.y.z.tar.gz

Alternatively, make sure you have ``just`` installed and run the following command:

::

    just local

[COMING SOON] Using a Docker image
----------------------------------

If you do not want to, or cannot, install all of the required software for this collection on your system, you may wish to build a Docker image that contains all of the software required to run Ansible playbooks which use this collection.

A Docker image, ``ghcr.io/COMING/SOON``, has been published to Docker Hub.

You can run a playbook using this Docker image, by volume mounting the playbook into the Docker container and running the ``ansible-playbook`` command:

::

    docker run --rm -u $(id -u) -v /path/to/playbooks:/playbooks ghcr.io/ibm-blockchain/ofs-ansibe:sha-826e86e ansible-playbook /playbooks/playbook.yml

Note that the UID flag ``-u $(id -u)`` ensures that Ansible can write connection profile and identity files to the volume mount.

The Docker image is supported for use in Docker, Kubernetes, and Red Hat OpenShift.

If you need to build or customize the Docker image, you can find the Dockerfile here: https://github.com/hyperledger-labs/fabric-ansible-collection/blob/main/Dockerfile

