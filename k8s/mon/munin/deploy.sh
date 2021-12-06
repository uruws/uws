#!/bin/sh
set -eu
~/k8s/mon/munin/configure.sh
VERSION="$(cat ~/k8s/mon/munin/VERSION)"
export VERSION
envsubst <~/k8s/mon/munin/deploy.yaml | uwskube apply -f -
exit 0
