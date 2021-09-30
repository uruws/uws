#!/bin/sh
set -eu

helm="helm --kubeconfig ${HOME}/.kube/eksctl/clusters/${UWS_CLUSTER}"

${helm} repo add jetstack https://charts.jetstack.io
${helm} repo update

uwskube create namespace cert-manager

${helm} install cert-manager jetstack/cert-manager \
	--namespace cert-manager \
	--version 1.3.0 \
	--set installCRDs=true

exit 0
