#!/bin/sh
set -eu
appver=${1:-''}
${HOME}/pod/meteor/infra-ui/configure.sh
exec ${HOME}/pod/meteor/deploy.sh infra-ui infra-ui ${appver}
