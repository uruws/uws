#!/bin/sh
set -eu
appver=${1:-''}
${HOME}/pod/meteor/web/configure.sh
export METEOR_NAMESPACE=api
exec ${HOME}/pod/meteor/deploy.sh web web "${appver}"
