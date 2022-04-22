#!/bin/sh
set -eu
appver=${1:-''}
export APP_REPLICAS="${METEOR_CS_REPLICAS}"
exec ${HOME}/pod/meteor/deploy.sh cs cs ${appver}
