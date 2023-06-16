#!/bin/sh
set -eu
ns=${1:?'namespace?'}
~/k8s/nginx/mkfs.sh "${ns}"
exit 0
