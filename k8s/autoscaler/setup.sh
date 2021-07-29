#!/bin/sh
set -eu

cluster=${UWS_CLUSTER}

#. ~/secret/secret.env

sed "s#\[UWS_CLUSTER]#${cluster}#" ~/k8s/autoscaler/deploy.yaml.in >/tmp/cluster-autoscaler-${cluster}.yaml

uwskube apply -f /tmp/cluster-autoscaler-${cluster}.yaml

#uwskube annotate serviceaccount cluster-autoscaler \
#	--namespace=kube-system \
#	eks.amazonaws.com/role-arn=arn:aws:iam::${AWS_ACCOUNT_ID}:role/eksClusterAutoscalerRole

uwskube patch deployment cluster-autoscaler --namespace=kube-system \
	-p '{"spec":{"template":{"metadata":{"annotations":{"cluster-autoscaler.kubernetes.io/safe-to-evict":"false"}}}}}'

exit 0
