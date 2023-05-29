#!/bin/sh
set -eu
~/k8s/mon/munin-node/configure.sh

VERSION="$(cat ~/k8s/mon/munin/VERSION)"
export VERSION

UWS_DEPLOY=$(date '+%y%m%d.%H%M%S')
export UWS_DEPLOY

envsubst <~/k8s/mon/munin-node/deploy.yaml | uwskube apply -f -
exit 0
