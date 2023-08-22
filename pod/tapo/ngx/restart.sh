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

gateway_configure "${nsorig}" "${cfgdir}"

~/k8s/nginx/restart.sh "${ns}" "${cfgdir}"

rm -rf "${cfgdir}"
exit 0
