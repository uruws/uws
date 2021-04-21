#!/bin/sh
set -eu
cluster=${UWS_CLUSTER}
kubectl="uwskube ${cluster}"
pod=/home/uws/pod/test
${kubectl} delete -f ${pod}/deploy.yaml
exit 0
