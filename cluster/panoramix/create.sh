#!/bin/sh
set -eu

uwseks-cluster-create --profile "${AWS_PROFILE}" --region "${AWS_REGION}" \
	--zones "${AWS_ZONES}" \
	--nodes 2 --nodes-min 2 --nodes-max 30 \
	--instance-types "${AWS_INSTANCE_TYPES}" \
	"${UWS_CLUSTER}"

uwseks-cluster-setup

~/k8s/ca/setup.sh

exit 0
