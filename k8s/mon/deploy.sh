#!/bin/sh
set -eu

cluster_env=${HOME}/.kube/eksctl/clusters/uwsdev

uwskube delete secret cluster-env -n mon || true
uwskube create secret generic cluster-env -n mon \
	--from-file="${UWS_CLUSTER}=${cluster_env}"

export VERSION="$(cat ~/k8s/VERSION)"
envsubst <~/k8s/mon/deploy.yaml | uwskube apply -f -

exit 0
