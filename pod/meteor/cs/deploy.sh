#!/bin/sh
set -eu
appver=${1:-''}
~/pod/meteor/cs/configure.sh "${METEOR_CS_ENV}"
export APP_REPLICAS="${METEOR_CS_REPLICAS}"
~/pod/meteor/deploy.sh cs cs "${appver}"
exec ~/pod/meteor/cs/gw/deploy.sh
