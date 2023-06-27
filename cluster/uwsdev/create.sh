#!/bin/sh
set -eu

nodes=3
nodes_min=3
nodes_max=100

uwseks-cluster-create --profile "${AWS_PROFILE}" --region "${AWS_REGION}" \
	--zones "${AWS_ZONES}" --k8s-version "${K8S_VERSION}" \
	--nodes "${nodes}" --nodes-min "${nodes_min}" --nodes-max "${nodes_max}" \
	--instance-types "${AWS_INSTANCE_TYPES}" \
	--spot "${UWS_CLUSTER}"

sleep 1

exit 0
