#!/bin/sh
set -eu
exec /usr/local/bin/helm.real --kubeconfig=${HOME}/.kube/eksctl/clusters/${UWS_CLUSTER} "$@"
