#!/bin/sh
set -eu

ec2_spot=${AWS_SPOT_INSTANCE:-"false"}

uwseks-cluster-create --profile "${AWS_PROFILE}" --region "${AWS_REGION}" \
	--zones "${AWS_ZONES}" --k8s-version "${K8S_VERSION}" \
	--nodes 5 --nodes-min 2 --nodes-max 300 \
	--instance-types "${AWS_INSTANCE_TYPES}" \
	--spot "${ec2_spot}" \
	"${UWS_CLUSTER}"

exit 0
