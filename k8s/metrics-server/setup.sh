#!/bin/sh
set -eu
uwskube kustomize ~/k8s/metrics-server/deploy/base | uwskube apply -f -
exit 0
