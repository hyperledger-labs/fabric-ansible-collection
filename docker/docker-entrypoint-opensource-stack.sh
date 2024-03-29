#!/usr/bin/env bash
#
# SPDX-License-Identifier: Apache-2.0
#
set -euo pipefail

# If this image is run with -u <random UID>, as happens on Red Hat OpenShift, then
# the user is not in the /etc/passwd file. This causes Ansible to fail, so we need
# to add the user to /etc/passwd now before Ansible runs.
if ! whoami &> /dev/null; then
    sed '/hlf-user/d' /etc/passwd > /tmp/passwd
    cat /tmp/passwd > /etc/passwd
    rm -f /tmp/passwd
    echo "hlf-user:x:$(id -u):0::/home/hlf-user:/bin/bash" >> /etc/passwd
    export HOME=/home/hlf-user
fi

# Run a shell or the specified command.
if [ $# -eq 0 ]; then
    exec /bin/bash
else
    exec "$@"
fi
