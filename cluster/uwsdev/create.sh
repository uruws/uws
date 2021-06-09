#!/bin/sh
set -eu
. ~/bin/env.export

nodes=2
nodes_min=2
nodes_max=10

uwseks-cluster-create --profile ${AWS_PROFILE} --region ${AWS_REGION} \
	--nodes ${nodes} --nodes-min ${nodes_min} --nodes-max ${nodes_max} \
	--instance-types "${AWS_INSTANCE_TYPES}" \
	${UWS_CLUSTER}

uwseks-cluster-setup
exit 0
