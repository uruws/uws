#!/bin/sh
set -eu

. ~/bin/env.export

cluster=${UWS_CLUSTER}
files=~/files
kubectl="kubectl --kubeconfig=~/.kube/eksctl/clusters/${cluster}"

${kubectl} delete -f ${files}/metrics-server.yaml

exit 0
