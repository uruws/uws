#!/bin/sh
set -eu
exec uwseks-cluster-create --profile "${AWS_PROFILE}" --region "${AWS_REGION}" \
	--nodes 3 --nodes-min 3 --nodes-max 50 \
	--instance-types "${AWS_INSTANCE_TYPES}" \
	"${UWS_CLUSTER}"
