#!/bin/sh
set -eu

# shellcheck source=/home/uws/k8s/mon/kubeshark/gw/configure.sh
. ~/k8s/mon/kubeshark/gw/configure.sh

cfgdir=$(mktemp -d -p /tmp kubeshark-gw-deploy-XXXXXXXXXX)

gateway_configure "${cfgdir}"

~/k8s/nginx/deploy.sh ksgw "${cfgdir}"

rm -rf "${cfgdir}"
exit 0
