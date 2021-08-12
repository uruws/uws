#!/bin/sh
set -eu
export VERSION="$(cat ~/k8s/mon/VERSION)"
envsubst <~/k8s/mon/munin-node/deploy.yaml | uwskube apply -f -
exit 0
