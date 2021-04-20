#!/bin/sh
set -eu

kubectl='kubectl --kubeconfig=/home/uws/.kube/eksctl/clusters/amybeta'
k8s=/home/uws/k8s
secret=/home/uws/secret
cluster=/home/uws/cluster/amybeta

set -x

uwseks-cluster-setup amybeta

uwseks-cluster-setup-dashboard amybeta
uwseks-cluster-setup-metrics-server amybeta
uwseks-cluster-setup-cert-manager amybeta
uwseks-cluster-setup-nginx-ingress amybeta

${kubectl} apply -f ${k8s}/acme-prod.yaml
${kubectl} apply -f ${cluster}/certificates.yaml

${kubectl} create secret generic basic-auth --from-file=auth=${secret}/auth
${kubectl} get secret basic-auth -o yaml
${kubectl} apply -f ${cluster}/gateway.yaml

uwseks-cluster-setup-alb amybeta

exit 0
