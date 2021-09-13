#!/bin/sh
set -eu
envsubst '${CLUSTER_HOST}' <~/k8s/gateway/gateway.yaml | uwskube apply -f -
exit 0
