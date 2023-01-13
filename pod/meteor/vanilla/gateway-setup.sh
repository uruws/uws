#!/bin/sh
set -eu

envsubst <${HOME}/pod/meteor/vanilla/gateway.yaml | uwskube apply -f -

./k8s/offline-page/deploy.sh
./k8s/offline-page/setup.sh meteor-vanilla

exit 0
