#!/bin/sh
set -eu
envsubst '${CLUSTER_HOST}' <~/k8s/mon/kubeshark/gateway.yaml | uwskube apply -f -
exit 0
