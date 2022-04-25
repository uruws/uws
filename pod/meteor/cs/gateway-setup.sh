#!/bin/sh
set -eu
envsubst <~/pod/meteor/cs/gateway.yaml | uwskube apply -f -
exit 0
