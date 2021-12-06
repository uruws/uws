#!/bin/sh
set -eu
~/k8s/ctl/eks/configure.sh
CTL_VERSION="$(cat ~/k8s/ctl/VERSION)"
export CTL_VERSION
envsubst <~/k8s/ctl/eks/jobs.yaml | uwskube apply -f -
exit 0
