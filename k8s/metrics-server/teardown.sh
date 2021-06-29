#!/bin/sh
set -eu
release=${1:-'release'}
uwskube kustomize ~/k8s/metrics-server/deploy/${release} | uwskube delete -f -
exit 0
