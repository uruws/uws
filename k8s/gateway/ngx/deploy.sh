#!/bin/sh
set -eu

# shellcheck source=/home/uws/k8s/gateway/ngx/configure.sh
. ~/k8s/gateway/ngx/configure.sh

cfgdir=$(mktemp -d -p /tmp k8s-gateway-ngx-deploy-XXXXXXXXXX)
gateway_configure "${cfgdir}"

~/k8s/nginx/deploy.sh default "${cfgdir}"

rm -rf "${cfgdir}"
exit 0
