#!/bin/sh
set -eu
appver=${1:-''}
${HOME}/pod/meteor/worker/configure.sh
export APP_REPLICAS=${METEOR_WORKER_REPLICAS}
exec ${HOME}/pod/meteor/deploy.sh worker worker ${appver}
