#!/bin/sh
set -eu
uwskube kustomize ~/k8s/metrics-server/deploy/base | uwskube delete -f -
exit 0
