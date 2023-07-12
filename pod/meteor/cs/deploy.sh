#!/bin/sh
set -eu
appver=${1:-''}
~/pod/meteor/cs/configure.sh "${METEOR_CS_ENV}"
export APP_REPLICAS="${METEOR_CS_REPLICAS}"
export APP_ENV="${METEOR_CS_ENV}"
~/pod/meteor/deploy.sh cs cs "${appver}"
exec ~/pod/meteor/cs/gw/deploy.sh
