#!/bin/sh
set -eu

export VERSION=1.19.2

envsubst <~/k8s/autoscaler/deploy.yaml | uwskube apply -f -

uwskube patch deployment cluster-autoscaler --namespace=kube-system \
	-p '{"spec":{"template":{"metadata":{"annotations":{"cluster-autoscaler.kubernetes.io/safe-to-evict":"false"}}}}}'

exit 0
