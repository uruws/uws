#!/bin/sh
set -eu
name=${1:-'uwsdev'}
kubectl="kubectl --kubeconfig=/home/uws/.kube/eksctl/clusters/${name}"
k8s=/home/uws/k8s

set -x

${kubectl} delete -f ${k8s}/gateway.yaml
${kubectl} delete -f ${k8s}/certificates.yaml
${kubectl} delete -f ${k8s}/acme-staging.yaml

uwseks-cluster-teardown-nginx-ingress ${name}
uwseks-cluster-teardown-cert-manager ${name}
uwseks-cluster-teardown-metrics-server ${name}
uwseks-cluster-teardown-dashboard ${name}

uwseks-cluster-delete --profile uwsdev --region us-west-2 --wait ${name}

exit 0
