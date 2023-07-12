#!/bin/sh
set -eu
ns=${1:?'namespace?'}
echo "** nginx: setup ${ns}"
#~ ~/k8s/nginx/mkfs.sh "${ns}"
exit 0
