#!/bin/sh
set -eu

envsubst '${CLUSTER_HOST}' <~/k8s/kubeshark/gateway.yaml | uwskube apply -f -

#~/k8s/mon/k8s/configure.sh

VERSION="$(cat ~/k8s/mon/VERSION)"
export VERSION
envsubst <~/k8s/mon/kubeshark/deploy.yaml | uwskube apply -f -

exit 0
