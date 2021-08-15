#!/bin/sh
set -eu
~/k8s/mon/munin/configure.sh
export VERSION="$(cat ~/k8s/mon/munin/VERSION)"
envsubst <~/k8s/mon/munin/deploy.yaml | uwskube apply -f -
exit 0
