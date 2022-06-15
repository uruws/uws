#!/bin/sh
set -eu
envsubst <${HOME}/cluster/gateway.yaml | uwskube apply -f -
exit 0
