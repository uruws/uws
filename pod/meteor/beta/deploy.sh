#!/bin/sh
set -eu
appver=${1:-''}
exec ${HOME}/pod/meteor/deploy.sh beta ${appver}
