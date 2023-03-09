#!/bin/sh
set -eu

nsorig="${1:?'namespace?'}"
ns="${nsorig}gw"

# shellcheck source=/home/uws/pod/meteor/gw/configure.sh
. ~/pod/meteor/gw/configure.sh

cfgdir=$(mktemp -d -p ${HOME}/tmp meteor-gw-rollin-XXXXXXXXXX)

if test -s "${HOME}/pod/meteor/${nsorig}/nginx.conf"; then
	cp -va "${HOME}/pod/meteor/${nsorig}/nginx.conf" "${cfgdir}/"
fi

gateway_configure "${ns}" "${cfgdir}"

~/k8s/nginx/rollin.sh "${ns}" "${cfgdir}"

rm -rf "${cfgdir}"
exit 0
