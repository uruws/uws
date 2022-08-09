#!/bin/sh
set -eu

APP_REPLICAS=${1:-3}
export APP_REPLICAS

APP_VERSION=$(cat ~/k8s/offline-page/VERSION)
export APP_VERSION

envsubst <~/k8s/offline-page/deploy.yaml | uwskube apply -f -

exit 0
