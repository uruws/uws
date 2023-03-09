#!/bin/sh
set -eu

ns="${1:?'namespace?'}gw"

# shellcheck source=/home/uws/pod/meteor/gw/configure.sh
. ~/pod/meteor/gw/configure.sh

cfgdir=$(mktemp -d -p ${HOME}/tmp meteor-gw-deploy-XXXXXXXXXX)

if test -s "${HOME}/pod/meteor/${ns}/nginx.conf"; then
	cp -va "${HOME}/pod/meteor/${ns}/nginx.conf" "${cfgdir}/"
fi

gateway_configure "${ns}" "${cfgdir}"

~/k8s/nginx/deploy.sh "${ns}" "${cfgdir}"

rm -rf "${cfgdir}"
exit 0
