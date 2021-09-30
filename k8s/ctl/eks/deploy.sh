#!/bin/sh
set -eu
~/k8s/ctl/eks/configure.sh
export CTL_VERSION="$(cat ~/k8s/ctl/VERSION)"
envsubst <~/k8s/ctl/eks/jobs.yaml | uwskube apply -f -
exit 0
