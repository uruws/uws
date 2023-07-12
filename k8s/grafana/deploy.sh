#!/bin/sh
set -eu
envsubst '${UWS_CLUSTER}' <~/secret/grafana/cloud-deploy.yaml | uwskube apply -f -
exit 0
