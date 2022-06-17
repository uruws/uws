#!/bin/sh
set -eu
envsubst <${HOME}/cluster/gateway.yaml | uwskube delete -f -
exit 0
