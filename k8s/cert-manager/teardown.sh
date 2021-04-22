#!/bin/sh
set -eu

. ~/bin/env.export

cluster=${UWS_CLUSTER}
kubectl="uwskube ${cluster}"
helm="helm --kubeconfig ~/.kube/eksctl/clusters/${cluster}"

${helm} uninstall --namespace cert-manager cert-manager
${kubectl} delete secret -n cert-manager acme-prod-account-key
${kubectl} delete namespace cert-manager

exit 0
