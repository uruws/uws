#!/bin/sh
set -eu

uwseks-cluster-create --profile "${AWS_PROFILE}" --region "${AWS_REGION}" \
	--zones "${AWS_ZONES}" --k8s-version "${K8S_VERSION}" \
	--nodes 10 --nodes-min 5 --nodes-max 100 \
	--instance-types "${AWS_INSTANCE_TYPES}" \
	--spot "${UWS_CLUSTER}"

sleep 3

exec uwseks-cluster-setup
