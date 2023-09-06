#!/bin/sh
set -eu
ns=${1:?'namespace?'}
uwskube create namespace "${ns}"
~/k8s/nginx/setup-ca.sh "${ns}"
exit 0
