#!/bin/sh
set -eu
. ~/bin/env.export

nodes=2
nodes_min=2
nodes_max=10
instance_types='t3a.small'

uwseks-cluster-create --profile ${AWS_PROFILE} --region ${AWS_REGION} \
	--nodes ${nodes} --nodes-min ${nodes_min} --nodes-max ${nodes_max} \
	--instance-types "${instance_types}" \
	${UWS_CLUSTER}

set -x
uwseks-cluster-setup
exit 0
