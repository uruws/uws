#!/bin/sh
set -eu
ns=${1:?'namespace?'}
replicas=${2:?'replicas?'}
exec ~/k8s/nginx/scale.sh "${ns}" "${replicas}"
