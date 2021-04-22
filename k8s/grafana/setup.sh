#!/bin/sh
set -eu

. ~/bin/env.export

cluster=${UWS_CLUSTER}
files=~/files
kubectl="kubectl --kubeconfig=~/.kube/eksctl/clusters/${cluster}"
helm="helm --kubeconfig ~/.kube/eksctl/clusters/${cluster}"

#~ ${kubectl} create namespace prometheus

${helm} repo add grafana https://grafana.github.io/helm-charts
${helm} repo update

${helm} upgrade -i loki-grafana grafana/grafana \
	--namespace prometheus

exit 0
