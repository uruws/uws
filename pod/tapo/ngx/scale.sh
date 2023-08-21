#!/bin/sh
set -eu
ns=${1:?'namespace?'}
pod=${2:?'pod?'}
replicas=${3:?'replicas?'}
exec ~/k8s/nginx/deploy.sh "${ns}" "${pod}" "${replicas}"
