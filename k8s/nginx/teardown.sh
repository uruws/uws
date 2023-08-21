#!/bin/sh
set -u
ns=${1:?'namespace?'}
uwskube delete service proxy -n "${ns}"
~/k8s/nginx/rmfs.sh "${ns}"
~/k8s/nginx/teardown-ca.sh "${ns}"
exit 0
