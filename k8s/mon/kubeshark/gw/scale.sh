#!/bin/sh
set -eu
replicas=${1:?'replicas?'}
exec ~/k8s/nginx/scale.sh ksgw "${replicas}"
