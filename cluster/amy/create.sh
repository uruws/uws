#!/bin/sh
set -eu

uwseks-cluster-create --profile "${AWS_PROFILE}" --region "${AWS_REGION}" \
	--zones "${AWS_ZONES}" \
	--nodes 10 --nodes-min 5 --nodes-max 90 \
	--instance-types "${AWS_INSTANCE_TYPES}" \
	"${UWS_CLUSTER}"

uwseks-cluster-setup

exit 0
