#!/bin/sh
set -eu

. ~/bin/env.export

helm="helm --kubeconfig ${HOME}/.kube/eksctl/clusters/${UWS_CLUSTER}"

${helm} repo add jetstack https://charts.jetstack.io
${helm} repo update

uwskube create namespace cert-manager

uwskube create secret generic -n cert-manager acme-prod-account-key \
	--from-file=tls.key=${HOME}/secret/acme/accounts/acme-v02.prod

${helm} install cert-manager jetstack/cert-manager \
	--namespace cert-manager \
	--version 1.3.0 \
	--set installCRDs=true

exit 0
