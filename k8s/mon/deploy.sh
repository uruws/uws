#!/bin/sh
set -eu

cluster_auth=${HOME}/.kube/eksctl/clusters/uwsdev

uwskube delete secret cluster-auth -n mon || true
uwskube create secret generic cluster-auth -n mon \
	--from-file="${UWS_CLUSTER}=${cluster_auth}"

cluster_env=$(mktemp uwsdev-env.XXXXXXXX)

echo "UWS_CLUSTER=${UWS_CLUSTER}" >${cluster_env}

uwskube delete configmap cluster-env -n mon || true
uwskube create configmap cluster-env -n mon \
	--from-env-file=${cluster_env}

rm -vf ${cluster_env}

export VERSION="$(cat ~/k8s/VERSION)"
envsubst <~/k8s/mon/deploy.yaml | uwskube apply -f -

exit 0
