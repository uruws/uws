#!/bin/sh
set -eu
appver=${1:-''}
${HOME}/pod/meteor/worker/configure.sh
exec ${HOME}/pod/meteor/deploy.sh worker ${appver}
