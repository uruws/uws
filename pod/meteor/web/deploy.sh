#!/bin/sh
set -eu
appver=${1:-''}

echo 'webcdn'
~/pod/meteor/webcdn/deploy.sh "${appver}"
~/pod/meteor/webcdn/wait.sh

echo 'web'
~/pod/meteor/web/configure.sh
~/pod/meteor/deploy.sh web web "${appver}"

echo 'web/gw'
~/pod/meteor/web/gw/deploy.sh "${APP_REPLICAS}"

exit 0
