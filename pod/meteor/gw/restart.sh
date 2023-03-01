#!/bin/sh
set -eu

ns=${1:?'namespace?'}

# shellcheck source=/home/uws/pod/meteor/gw/configure.sh
. ~/pod/meteor/gw/configure.sh

cfgdir=$(mktemp -d -p ${HOME}/tmp meteor-gw-restart-XXXXXXXXXX)
gateway_configure "${ns}" "${cfgdir}"

~/k8s/nginx/restart.sh "${ns}" "${cfgdir}"

rm -rf "${cfgdir}"
exit 0
