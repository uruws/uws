#!/bin/sh
set -eu
~/k8s/mon/k8s/configure.sh

VERSION="$(cat ~/k8s/mon/VERSION)"
export VERSION

UWS_DEPLOY=$(date '+%y%m%d.%H%M%S')
export UWS_DEPLOY

envsubst <~/k8s/mon/k8s/deploy.yaml | uwskube apply -f -
exit 0
