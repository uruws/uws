#!/bin/sh
set -eu

. ~/k8s/gateway/configure.sh

cfgdir=$(mktemp -d -p ${HOME}/tmp k8s-gateway-deploy-XXXXXXXXXX)
gateway_configure "${cfgdir}"

~/k8s/nginx/deploy.sh default "${cfgdir}"

rm -rf "${cfgdir}"
exit 0
