#!/bin/sh
set -eu

. ~/bin/env.export

cluster=${UWS_CLUSTER}
files=~/files
kubectl="kubectl --kubeconfig=~/.kube/eksctl/clusters/${cluster}"

# FIXME: teardown k8s-dashboard fails
${kubectl} delete -f ${files}/k8s-dashboard.yaml

${kubectl} delete -f ${files}/k8s-dashboard-auth.yaml

exit 0
