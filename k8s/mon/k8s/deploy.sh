#!/bin/sh
set -eu
~/k8s/mon/k8s/configure.sh
export VERSION="$(cat ~/k8s/mon/VERSION)"
envsubst <~/k8s/mon/k8s/deploy.yaml | uwskube apply -f -
exit 0
