#!/bin/sh
set -eu

envsubst <${HOME}/k8s/autoscaler/${K8S_VERSION}/deploy.yaml | uwskube apply -f -

uwskube patch deployment cluster-autoscaler --namespace=kube-system \
	-p '{"spec":{"template":{"metadata":{"annotations":{"cluster-autoscaler.kubernetes.io/safe-to-evict":"false"}}}}}'

exit 0
