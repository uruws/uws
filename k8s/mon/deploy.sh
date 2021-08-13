#!/bin/sh
set -eu
export VERSION="$(cat ~/k8s/VERSION)"
envsubst <~/k8s/mon/deploy.yaml | uwskube apply -f -
exit 0
