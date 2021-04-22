#!/bin/sh
set -eu

. ~/bin/env.export

cluster=${UWS_CLUSTER}
kubectl="uwskube ${cluster}"
helm="helm --kubeconfig ~/.kube/eksctl/clusters/${cluster}"
secret=~/secret

${helm} repo add jetstack https://charts.jetstack.io
${helm} repo update

${kubectl} create namespace cert-manager

${kubectl} create secret generic -n cert-manager acme-prod-account-key \
	--from-file=tls.key=${secret}/acme/accounts/acme-v02.prod

${helm} install cert-manager jetstack/cert-manager \
	--namespace cert-manager \
	--version 1.3.0 \
	--set installCRDs=true

exit 0
