#!/usr/bin/env bash
set -euo pipefail
VERSION=$(yq -r .version galaxy.yml)
cd tutorial
TEST_RUN_ID=$(dd if=/dev/urandom bs=4096 count=1 2>/dev/null | shasum | awk '{print $1}')
SHORT_TEST_RUN_ID=$(echo "${TEST_RUN_ID}" | awk '{print substr($1,1,8)}')
yq -yi ".ordering_org_name=\"Ordering Org ${SHORT_TEST_RUN_ID}\"" common-vars.yml
yq -yi ".ordering_service_name=\"Ordering Service ${SHORT_TEST_RUN_ID}\"" common-vars.yml
yq -yi ".org1_name=\"Org1 ${SHORT_TEST_RUN_ID}\"" common-vars.yml
yq -yi ".org1_msp_id=\"Org1${SHORT_TEST_RUN_ID}MSP\"" common-vars.yml
yq -yi ".org2_name=\"Org2 ${SHORT_TEST_RUN_ID}\"" common-vars.yml
yq -yi ".org2_msp_id=\"Org2${SHORT_TEST_RUN_ID}MSP\"" common-vars.yml
yq -yi ".ordering_service_msp=\"Orderer${SHORT_TEST_RUN_ID}MSP\"" ordering-org-vars.yml
yq -yi ".org1_ca_name=\"Org1 CA ${SHORT_TEST_RUN_ID}\"" org1-vars.yml
yq -yi ".org1_peer_name=\"Org1 Peer ${SHORT_TEST_RUN_ID}\"" org1-vars.yml
yq -yi ".org2_ca_name=\"Org2 CA ${SHORT_TEST_RUN_ID}\"" org2-vars.yml
yq -yi ".org2_peer_name=\"Org2 Peer ${SHORT_TEST_RUN_ID}\"" org2-vars.yml
for VARS in ordering-org-vars.yml org1-vars.yml org2-vars.yml; do
    yq -yi ".api_endpoint=\"${API_ENDPOINT}\"" ${VARS}
    yq -yi ".api_authtype=\"${API_AUTHTYPE}\"" ${VARS}
    yq -yi ".api_key=\"${API_KEY}\"" ${VARS}
    yq -yi ".api_secret=\"${API_SECRET}\"" ${VARS}
    yq -yi ".api_timeout=300" ${VARS}
    yq -yi ".k8s_namespace=\"${K8S_NAMESPACE}\"" ${VARS}
    yq -yi ".wait_timeout=1800" ${VARS}
done
if [ "${USE_DOCKER}" = "true" ]; then
    function docker_cleanup {
        docker run --rm -e IBP_ANSIBLE_LOG_FILENAME -u "$(id -u)" -v "${PWD}:/tutorial" -v /tmp:/tmp "ibmcom/ibp-ansible:${VERSION}" /tutorial/join_network.sh destroy
    }
    trap docker_cleanup EXIT
    docker run --rm -e IBP_ANSIBLE_LOG_FILENAME -u "$(id -u)" -v "${PWD}:/tutorial" -v /tmp:/tmp "ibmcom/ibp-ansible:${VERSION}" /tutorial/build_network.sh build
    docker run --rm -e IBP_ANSIBLE_LOG_FILENAME -u "$(id -u)" -v "${PWD}:/tutorial" -v /tmp:/tmp "ibmcom/ibp-ansible:${VERSION}" /tutorial/join_network.sh join
    docker run --rm -e IBP_ANSIBLE_LOG_FILENAME -u "$(id -u)" -v "${PWD}:/tutorial" -v /tmp:/tmp "ibmcom/ibp-ansible:${VERSION}" /tutorial/deploy_smart_contract.sh
    trap - EXIT
    docker_cleanup
else
    function cleanup {
        ./join_network.sh destroy
    }
    trap cleanup EXIT
    ./build_network.sh build
    ./join_network.sh join
    ./deploy_smart_contract.sh
    trap - EXIT
    ./join_network.sh destroy
fi