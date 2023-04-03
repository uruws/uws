#!/bin/sh
set -eu

# shellcheck source=/home/uws/k8s/mon/kubeshark/gw/configure.sh
. ~/k8s/mon/kubeshark/gw/configure.sh

cfgdir=$(mktemp -d -p /tmp kubeshark-gw-rollin-XXXXXXXXXX)

gateway_configure ksgw "${cfgdir}"

~/k8s/nginx/rollin.sh ksgw "${cfgdir}"

rm -rf "${cfgdir}"
exit 0
