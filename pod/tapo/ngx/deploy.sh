#!/bin/sh
set -eu

nsorig="${1:?'namespace?'}"
pod="${2:?'pod?'}"

ns="${nsorig}gw"

# shellcheck source=/home/uws/pod/tapo/ngx/configure.sh
. ~/pod/tapo/ngx/configure.sh

cfgdir=$(mktemp -d -p /tmp "tapo-ngx-${ns}-deploy-XXXXXXXXXX")

if test -s "${HOME}/pod/${pod}/nginx.conf"; then
	cp -va "${HOME}/pod/${pod}/nginx.conf" "${cfgdir}/"
fi

if test -s "${HOME}/pod/${pod}/ngx/meteor-backend-configure.sh"; then
	cp -va "${HOME}/pod/${pod}/ngx/meteor-backend-configure.sh" "${cfgdir}/"
fi

if test -s "${HOME}/pod/${pod}/ngx/meteor-service-configure.sh"; then
	cp -va "${HOME}/pod/${pod}/ngx/meteor-service-configure.sh" "${cfgdir}/"
fi

gateway_configure "${nsorig}" "${cfgdir}"

~/k8s/nginx/deploy.sh "${ns}" "${cfgdir}"

rm -rf "${cfgdir}"
exit 0