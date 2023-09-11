#!/bin/sh
set -eu

EXTRA_ARGS=""
ec2_spot=${AWS_SPOT_INSTANCE:-""}
if test "X${ec2_spot}" = 'Xtrue'; then
	EXTRA_ARGS='--spot'
fi

uwseks-cluster-create --profile "${AWS_PROFILE}" --region "${AWS_REGION}" \
	--zones "${AWS_ZONES}" --k8s-version "${K8S_VERSION}" \
	--nodes 5 --nodes-min 2 --nodes-max 300 \
	--instance-types "${AWS_INSTANCE_TYPES}" \
	${EXTRA_ARGS} "${UWS_CLUSTER}"

exit 0
