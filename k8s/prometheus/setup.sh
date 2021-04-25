#!/bin/sh
set -eu

. ~/bin/env.export

helm="helm --kubeconfig ${HOME}/.kube/eksctl/clusters/${UWS_CLUSTER}"

uwskube create namespace prometheus

${helm} repo add prometheus-community https://prometheus-community.github.io/helm-charts
${helm} repo update

${helm} upgrade -i prometheus prometheus-community/prometheus \
	--namespace prometheus \
	--set alertmanager.persistentVolume.storageClass="gp2" \
	--set server.persistentVolume.storageClass="gp2"

exit 0
