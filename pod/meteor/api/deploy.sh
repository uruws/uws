#!/bin/sh
set -eu
appver=${1:-''}
~/pod/meteor/api/configure.sh
export APP_REPLICAS=${METEOR_API_REPLICAS}
export APP_CPU=${METEOR_API_CPU}
export APP_MEMORY=${METEOR_API_MEMORY}
export APP_NAMESPACE=api
~/pod/meteor/deploy.sh api web "${appver}"
exit 0
