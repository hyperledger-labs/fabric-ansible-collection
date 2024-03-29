# Hyperledger Fabric Ansible Collection

Hyperledger Fabric is an open source, industry standard, blockchain technology that allows you to build, operate & govern and grow enterprise blockchain networks. This Ansible collection enables you to automate the building of Hyperledger Fabric networks.

*Please Note* the main branch is now set to `2.0.0-beta`, the `release-1.2` branch is available. If you build a local copy of Ansible for production, please work from the `release-1.2` branch.

## Beta support for Fabric Operator and Fabric Operations Console

With the Open Source version of the [Fabric Operations Console](https://github.com/hyperledger-labs/fabric-operations-console) and the [Fabric Operator](https://github.com/hyperledger-labs/fabric-operator), it is possible now to use the Ansible Playbooks previously targetted towards The IBM Blockchain Platform in a complete open source stack.

This should be considered beta functionality at present, please do try it out, but would not advise production use cases at present. Both the Operator AND the Console must be installed.

Currently the installation of the Operator and Console are available via Playbooks. Once installed Fabric resources can be managed with the existing Ansible modules.

Please see the [README](./examples/opensource-stack/README.md) in the `opensource-stack` example for more information.

## Noteable Updates

- Added support for deploying both the Open Source and HLF Support console and operator on IKS v1.25
- Added a chaincode information module `chaincode_list_info` to get details of chaincodes in a peer
- Added ability to handle automatic sequence numbers in the approved chaincode module. See the [example](./examples/chaincode_info/00-org1-chaincode-info.yml) playbook for how to use these two new chaincode abilities.

## Using the collection

The choice will depend on what context you want to use ansible in.

- If you've existing Ansible configurations you can install the v1.2 collection via `ansible-galaxy collection install hyperledger.fabric-ansible-collection`. For v2 install from source (see next option).
- Install from source; clone this github repo, and run

```shell
    ansible-galaxy collection build -f
    ansible-galaxy collection install $(ls -1 | grep fabric_ansible_collection) -f
```

- Using a Docker container.
  <!-- For v1.2, a Docker image, ``ibmcom/ibp-ansible``, has been published to Docker Hub. -->

  <!-- You can run a playbook using this Docker image, by volume mounting the playbook into the Docker container and running the ``ansible-playbook`` command: -->

  <!-- ```shell
  docker run --rm -u $(id -u) -v /path/to/playbooks:/playbooks ibmcom/ibp-ansible ansible-playbook /playbooks/playbook.yml
  ``` -->

    <!-- Note that the UID flag ``-u $(id -u)`` ensures that Ansible can write connection profile and identity files to the volume mount. -->

  For v2.0, the docker image is in the `ghcr.io` [registry](https://github.com/hyperledger-labs/fabric-ansible-collection/pkgs/container/fabric-ansible). It can be run in the same way

  ```shell
  docker pull ghcr.io/hyperledger-labs/fabric-ansible:sha-c9330b9
  docker run --rm -u $(id -u) -v /path/to/playbooks:/playbooks ghcr.io/hyperledger-labs/fabric-ansible:sha-c9330b9 ansible-playbook /playbooks/playbook.yml
  ```
- For running in environments like ubuntu that does not have the ibp-user (open source stack) you need to override the docker entrypoint:
  ```shell
  docker run --entrypoint docker/docker-entrypoint-opensource-stack.sh --rm -u $(id -u) -v /path/to/playbooks:/playbooks ghcr.io/hyperledger-labs/fabric-ansible:sha-c9330b9 ansible-playbook /playbooks/playbook.yml
  ```

- If you are using minikube with docker driver you need to specify the docker minikube network:
  ```shell
  docker run --network minikube --entrypoint docker/docker-entrypoint-opensource-stack.sh --rm -u $(id -u) -v /path/to/playbooks:/playbooks ghcr.io/hyperledger-labs/fabric-ansible:sha-c9330b9 ansible-playbook /playbooks/playbook.yml
  ```

- If you are using github actions for CI/CD there is a [github action](https://github.com/hyperledgendary/fabric-cloud-infrastructure/tree/main/fabric-ansible-action) that uses the same docker image as the basis.
  For example; note this action needs to still be published. In the interim please copy this to your own repository

  ```yaml
    - name: Create the Fabric CRDs/Operator
      id: operatorinstall
      uses: ./fabric-ansible-action
      with:
        playbook: playbooks/operator_console_playbooks/01-operator-install.yml
  ```

## Documentation

Documentation for this Ansible collection is available here: <https://labs.hyperledger.org/fabric-ansible-collection/>

The documentation includes installation instructions, tutorials, and reference material for all modules and roles in this collection.

## License

Apache-2.0
