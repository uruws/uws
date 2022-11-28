#!/bin/sh
set -eu
~/k8s/mon/k8s/configure.sh
VERSION="$(cat ~/k8s/mon/VERSION)"
export VERSION
envsubst <~/k8s/mon/kubeshark/deploy.yaml | uwskube apply -f -
exit 0
