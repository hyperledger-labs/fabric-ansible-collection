docker run -it --rm -u $(id -u) -v "local fully qualified path to fabproxy removal playbooks":/playbooks ghcr.io/hyperledger-labs/fabric-ansible:sha-c9330b9 bash

docker pull ghcr.io/hyperledger-labs/fabric-ansible:sha-c9330b9
docker run --rm -u $(id -u) -v /path/to/playbooks:/playbooks ghcr.io/hyperledger-labs/fabric-ansible:sha-c9330b9 ansible-playbook /playbooks/playbook.yml