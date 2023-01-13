#!/bin/sh
set -eu
appver=${1:-''}
${HOME}/pod/meteor/web/configure.sh
export APP_NAMESPACE=web
exec ${HOME}/pod/meteor/deploy.sh web web "${appver}"
