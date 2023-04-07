#!/bin/sh
set -eu
envsubst '${UWS_CLUSTER}' <~/secret/grafana/configure.yaml | uwskube apply -f -
exit 0
