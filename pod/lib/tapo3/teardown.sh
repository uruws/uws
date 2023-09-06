#!/bin/sh
set -u
ns=${1:?'namespace?'}
~/k8s/nginx/teardown-ca.sh "${ns}"
uwskube delete namespace "${ns}"
exit 0
