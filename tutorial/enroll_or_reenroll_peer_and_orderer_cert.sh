#!/usr/bin/env bash
set -e
cd "$(dirname "$0")"
IMPORT_EXPORT_REQUIRED=0
function usage {
    echo "Usage: renew_certificate.sh [-i] [-i <component Type>] [-j <certificate Type>] [-k <action>]" 1>&2
    exit 1
}
OPTSTRING=":i:j:k:"

while getopts ${OPTSTRING} opt; do
    case "${opt}" in
        i)
            component_type=${OPTARG}
            IMPORT_EXPORT_REQUIRED=1
            ;;
        j)
            cert_type=${OPTARG}
            IMPORT_EXPORT_REQUIRED=1
            ;;
        k)
            action=${OPTARG}
            IMPORT_EXPORT_REQUIRED=1
            ;;
        *)
            usage
            ;;
    esac
done
shift $((OPTIND-1))
if [ -z "${component_type}" ] || [ -z "${cert_type}" ] || [ -z "${action}" ]; then
    usage
fi
if [ "${component_type}" = "peer" ]; then
    set -x
    if [ "${cert_type}" = "ecert" ]; then
        ansible-playbook 24-reenroll-peer-tls-and-ecert.yml --extra-vars '{"cert_type":'${cert_type}',"action":'${action}'}'
    else
        ansible-playbook 24-reenroll-peer-tls-and-ecert.yml --extra-vars '{"cert_type":'${cert_type}',"action":'${action}'}'
    fi

    set +x
elif [ "${component_type}" = "orderer" ]; then
    set -x
    if [ "${cert_type}" = "ecert" ]; then
        ansible-playbook 25-reenroll-orderer-tls-and-ecert.yml --extra-vars '{"cert_type":'${cert_type}',"action":'${action}'}'
    else
        ansible-playbook 25-reenroll-orderer-tls-and-ecert.yml --extra-vars '{"cert_type":'${cert_type}',"action":'${action}'}'
    fi
    set +x
elif [ "${component_type}" = "ca" ]; then
    set -x
    ansible-playbook 26-renew-all-ca-tls.yml
    set +x
fi
echo "s = ${component_type}"
echo "p = ${cert_type}"

