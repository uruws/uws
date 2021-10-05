#!/bin/sh
set -eu

export VERSION="${K8S_AUTOSCALER:-1.19.1}"
echo "VERSION=${VERSION}"

envsubst <~/k8s/autoscaler/deploy.yaml | uwskube apply -f -

uwskube patch deployment cluster-autoscaler --namespace=kube-system \
	-p '{"spec":{"template":{"metadata":{"annotations":{"cluster-autoscaler.kubernetes.io/safe-to-evict":"false"}}}}}'

exit 0
