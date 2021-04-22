#!/bin/sh
set -eu

. ~/bin/env.export

cluster=${UWS_CLUSTER}
files=~/files
kubectl="kubectl --kubeconfig=~/.kube/eksctl/clusters/${cluster}"
helm="helm --kubeconfig ~/.kube/eksctl/clusters/${cluster}"

${helm} uninstall loki-grafana --namespace prometheus

exit 0
