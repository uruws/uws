#!/bin/sh
set -eu
envsubst '${CLUSTER_HOST}' <~/k8s/mon/dashboard/gateway.yaml | uwskube apply -f -
exit 0
