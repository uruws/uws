#!/bin/sh
set -eu
appver=${1:-''}
${HOME}/pod/meteor/beta/configure.sh
exec ${HOME}/pod/meteor/deploy.sh meteor-beta ${appver}
