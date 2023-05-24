#!/bin/sh
set -eu
appver=${1:-''}
~/pod/meteor/worker/configure.sh
export APP_REPLICAS=${METEOR_WORKER_REPLICAS}
exec ~/pod/meteor/deploy.sh worker worker ${appver}
