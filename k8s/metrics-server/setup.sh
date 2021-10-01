#!/bin/sh
set -eu
exec uwskube kustomize ~/k8s/metrics-server/deploy/release | uwskube apply -f -
