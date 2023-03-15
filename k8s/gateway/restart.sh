#!/bin/sh
set -eu

# shellcheck source=/home/uws/k8s/gateway/configure.sh
. ~/k8s/gateway/configure.sh

cfgdir=$(mktemp -d -p ${HOME}/tmp k8s-gateway-restart-XXXXXXXXXX)
gateway_configure "${cfgdir}"

~/k8s/nginx/restart.sh default "${cfgdir}"

rm -rf "${cfgdir}"
exit 0
