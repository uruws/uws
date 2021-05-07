#!/bin/sh
set -eu

. ~/bin/env.export

helm="helm --kubeconfig ${HOME}/.kube/eksctl/clusters/${UWS_CLUSTER}"

${helm} uninstall prometheus --namespace prometheus

uwskube delete namespace prometheus

exit 0
