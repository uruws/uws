#!/bin/sh
set -eu

# aws auth

aws_conf=${HOME}/.aws/config
aws_auth=${HOME}/.aws/credentials

uwskube delete secret aws-auth -n ctl || true
uwskube create secret generic aws-auth -n ctl \
	--from-file="config=${aws_conf}" \
	--from-file="credentials=${aws_auth}"

# cluster auth

cluster_auth=${HOME}/.kube/eksctl/clusters/${UWS_CLUSTER}

uwskube delete secret cluster-auth -n ctl || true
uwskube create secret generic cluster-auth -n ctl \
	--from-file="${UWS_CLUSTER}=${cluster_auth}"

# cluster env

cluster_env=$(mktemp eksctl-cluster-env.XXXXXXXX)

echo "UWS_CLUSTER=${UWS_CLUSTER}" >${cluster_env}
echo "AWS_PROFILE=${AWS_PROFILE}" >>${cluster_env}
echo "K8S_VERSION=${K8S_VERSION}" >>${cluster_env}

uwskube delete configmap cluster-env -n ctl || true
uwskube create configmap cluster-env -n ctl \
	--from-env-file=${cluster_env}

rm -f ${cluster_env}

exit 0
