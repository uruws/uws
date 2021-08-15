#!/bin/sh
set -eu
~/k8s/mon/munin-node/configure.sh
export VERSION="$(cat ~/k8s/mon/munin/VERSION)"
envsubst <~/k8s/mon/munin-node/deploy.yaml | uwskube apply -f -
exit 0
