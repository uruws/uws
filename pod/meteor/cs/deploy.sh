#!/bin/sh
set -eu
appver=${1:-''}
~/pod/meteor/cs/configure.sh "${METEOR_CS_ENV}"
export APP_REPLICAS="${METEOR_CS_REPLICAS}"
exec ${HOME}/pod/meteor/deploy.sh cs cs "${appver}"
