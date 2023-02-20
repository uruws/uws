#!/bin/sh
set -eu
cfgdir=$(mktemp -d -p ${HOME}/tmp k8s-gateway-XXXXXXXXXX)

install -v -d -m 0750 "${cfgdir}"
install -v -d -m 0750 "${cfgdir}/nginx"
install -v -d -m 0750 "${cfgdir}/nginx/sites-enabled"

envsubst <~/k8s/gateway/cluster.conf >"${cfgdir}/nginx/sites-enabled/cluster-gateway"

~/k8s/nginx/deploy.sh default "${cfgdir}"

rm -rf "${cfgdir}"
exit 0
