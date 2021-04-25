#!/bin/sh
set -eu

. ~/bin/env.export

helm="helm --kubeconfig ${HOME}/.kube/eksctl/clusters/${UWS_CLUSTER}"

${helm} uninstall --namespace cert-manager cert-manager

uwskube delete secret -n cert-manager acme-prod-account-key
uwskube delete namespace cert-manager

exit 0
