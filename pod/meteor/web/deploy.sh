#!/bin/sh
set -eu
appver=${1:-''}
${HOME}/pod/meteor/web/configure.sh
exec ${HOME}/pod/meteor/deploy.sh web web ${appver}
