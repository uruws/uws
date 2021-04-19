#!/bin/sh
set -eu
name=${1:-'uwsdev'}
kubectl="kubectl --kubeconfig=/home/uws/.kube/eksctl/clusters/${name}"
k8s=/home/uws/k8s
secret=/home/uws/secret
cluster=/home/uws/cluster/${name}

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
${kubectl} apply -f ${cluster}/certificates.yaml

${kubectl} create secret generic basic-auth --from-file=auth=${secret}/auth
${kubectl} get secret basic-auth -o yaml
${kubectl} apply -f ${cluster}/gateway.yaml

exit 0
