#!/bin/sh
set -eu
envsubst <${HOME}/cluster/gateway.yaml | uwskube apply -f -
~/k8s/offline-page/deploy.sh
~/k8s/offline-page/setup.sh web-gateway
exit 0
