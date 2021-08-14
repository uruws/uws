#!/bin/sh
set -eu

# aws auth

aws_conf=${HOME}/.aws/config
aws_auth=${HOME}/.aws/credentials

uwskube delete secret aws-auth -n mon || true
uwskube create secret generic aws-auth -n mon \
	--from-file="config=${aws_conf}" \
	--from-file="credentials=${aws_auth}"

# cluster auth

cluster_auth=${HOME}/.kube/eksctl/clusters/uwsdev

uwskube delete secret cluster-auth -n mon || true
uwskube create secret generic cluster-auth -n mon \
	--from-file="${UWS_CLUSTER}=${cluster_auth}"

# cluster env

cluster_env=$(mktemp uwsdev-env.XXXXXXXX)

echo "UWS_CLUSTER=${UWS_CLUSTER}" >${cluster_env}

uwskube delete configmap cluster-env -n mon || true
uwskube create configmap cluster-env -n mon \
	--from-env-file=${cluster_env}

rm -f ${cluster_env}

export VERSION="$(cat ~/k8s/mon/VERSION)"
envsubst <~/k8s/mon/k8s/deploy.yaml | uwskube apply -f -

exit 0
