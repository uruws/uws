#!/bin/sh
set -eu
appver=${1:-''}
~/pod/meteor/worker/configure.sh
export APP_REPLICAS=${METEOR_WORKER_REPLICAS}
~/pod/meteor/deploy.sh worker worker ${appver}
~/pod/meteor/worker/gw/deploy.sh
exit 0
