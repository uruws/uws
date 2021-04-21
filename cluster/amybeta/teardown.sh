#!/bin/sh
set -eu

kubectl='kubectl --kubeconfig=/home/uws/.kube/eksctl/clusters/amybeta'
k8s=/home/uws/k8s
cluster=/home/uws/cluster/amybeta

set -x

# FIXME: teardown of cluster gateway removes AWS load balancer
${kubectl} delete secret basic-auth
${kubectl} delete -f ${cluster}/gateway.yaml

${kubectl} delete -f ${cluster}/certificates.yaml
${kubectl} delete -f ${k8s}/acme.yaml

# FIXME: teardown nginx-ingress fails
uwseks-cluster-teardown-nginx-ingress amybeta

uwseks-cluster-teardown-cert-manager amybeta
uwseks-cluster-teardown-metrics-server amybeta
uwseks-cluster-teardown-dashboard amybeta

uwseks-cluster-teardown amybeta
exit 0
