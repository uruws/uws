#!/bin/sh
set -eu
appver=${1:-''}
~/pod/meteor/web/configure.sh
export APP_NAMESPACE=web
~/pod/meteor/deploy.sh web web "${appver}"
~/pod/meteor/web/gw/deploy.sh
exit 0
