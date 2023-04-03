#!/bin/sh
set -eu

nsorig="${1:?'namespace?'}"
ns="${nsorig}gw"

# shellcheck source=/home/uws/pod/meteor/gw/configure.sh
. ~/pod/meteor/gw/configure.sh

cfgdir=$(mktemp -d -p /tmp meteor-gw-restart-XXXXXXXXXX)

if test -s "${HOME}/pod/meteor/${nsorig}/nginx.conf"; then
	cp -va "${HOME}/pod/meteor/${nsorig}/nginx.conf" "${cfgdir}/"
fi

gateway_configure "${ns}" "${cfgdir}"

~/k8s/nginx/restart.sh "${ns}" "${cfgdir}"

rm -rf "${cfgdir}"
exit 0
