#!/bin/sh
set -eu
appver=${1:-''}
${HOME}/pod/meteor/api/configure.sh
export METEOR_NAMESPACE=api
exec ${HOME}/pod/meteor/deploy.sh api web "${appver}"
