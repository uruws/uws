#!/bin/sh
set -u
envsubst '${UWS_CLUSTER}' <~/secret/grafana/configure.yaml | uwskube delete -f -
exec uwskube delete namespace grfn
