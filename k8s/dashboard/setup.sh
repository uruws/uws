#!/bin/sh
set -eu

. ~/bin/env.export

cluster=${UWS_CLUSTER}
files=~/files
kubectl="kubectl --kubeconfig=~/.kube/eksctl/clusters/${cluster}"

${kubectl} apply -f ${files}/k8s-dashboard.yaml
${kubectl} apply -f ${files}/k8s-dashboard-auth.yaml

exit 0
