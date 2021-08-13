#!/bin/sh
set -eu
envsubst <~/k8s/gateway/gateway.yaml | uwskube apply -f -
exit 0
