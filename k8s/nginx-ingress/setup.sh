#!/bin/sh
set -eu
. ~/bin/env.export
cluster=${UWS_CLUSTER}
kubectl="kubectl --kubeconfig=~/.kube/eksctl/clusters/${cluster}"
files=~/files
${kubectl} apply -f ${files}/nginx-ingress.yaml
exit 0
