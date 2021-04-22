#!/bin/sh
set -eu

. ~/bin/env.export

cluster=${UWS_CLUSTER}
files=~/files
kubectl="kubectl --kubeconfig=~/.kube/eksctl/clusters/${cluster}"
helm="helm --kubeconfig ~/.kube/eksctl/clusters/${cluster}"

${kubectl} create namespace prometheus

${helm} repo add prometheus-community https://prometheus-community.github.io/helm-charts
${helm} repo update

${helm} upgrade -i prometheus prometheus-community/prometheus \
	--namespace prometheus \
	--set alertmanager.persistentVolume.storageClass="gp2",server.persistentVolume.storageClass="gp2"

exit 0
