#!/bin/sh
set -eu
appver=${1:-''}
~/pod/meteor/web/configure.sh
export APP_NAMESPACE=web
exec ~/pod/meteor/deploy.sh web web "${appver}"
