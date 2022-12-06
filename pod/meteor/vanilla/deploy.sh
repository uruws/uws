#!/bin/sh
set -eu
appver=${1:-''}
${HOME}/pod/meteor/vanilla/configure.sh
exec ${HOME}/pod/meteor/deploy.sh meteor-vanilla meteor-vanilla "${appver}"
