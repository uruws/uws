#!/bin/sh
set -eu
name=${1:-'uwsdev'}
kubectl="kubectl --kubeconfig=/home/uws/.kube/eksctl/clusters/${name}"
k8s=/home/uws/k8s

set -x

uwseks-cluster-create --profile uwsdev --region us-west-2 \
	--nodes 2 --nodes-min 2 --nodes-max 10 \
	--instance-types t3a.small \
	${name}

uwseks-cluster-setup-dashboard ${name}
uwseks-cluster-setup-metrics-server ${name}
uwseks-cluster-setup-cert-manager ${name}
uwseks-cluster-setup-nginx-ingress ${name}

${kubectl} apply -f ${k8s}/acme-staging.yaml
${kubectl} apply -f ${k8s}/certificates.yaml
${kubectl} apply -f ${k8s}/gateway.yaml

exit 0
