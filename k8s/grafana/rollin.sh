#!/bin/sh
set -u
envsubst '${UWS_CLUSTER}' <~/secret/grafana/cloud-deploy.yaml | uwskube delete -f -
exit 0
