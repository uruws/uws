#!/bin/sh
set -eu

name=${1:-'uwsdev'}
kubectl="kubectl --kubeconfig=/home/uws/.kube/eksctl/clusters/${name}"
k8s=/home/uws/k8s
cluster=/home/uws/cluster/${name}

set -x

${kubectl} delete secret basic-auth
${kubectl} delete -f ${cluster}/gateway.yaml

${kubectl} delete -f ${cluster}/certificates.yaml
${kubectl} delete -f ${k8s}/acme-staging.yaml

uwseks-cluster-teardown-nginx-ingress ${name}
uwseks-cluster-teardown-cert-manager ${name}
uwseks-cluster-teardown-metrics-server ${name}
uwseks-cluster-teardown-dashboard ${name}

exit 0
