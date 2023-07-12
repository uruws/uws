#!/bin/sh
set -eu

uws_cluster=uwsdev
#~ uws_cluster=${1:?'cluster?'}
#~ shift

eksenv=${PWD}/eks/env/${uws_cluster}.env
awsdir=${PWD}/secret/eks/aws/admin/${uws_cluster}

kubedir=${PWD}/secret/eks/kube/cluster/${uws_cluster}
mkdir -vp ${kubedir}

# shellcheck disable=SC1090
. ${eksenv}

hostname="${uws_cluster}.${AWS_REGION}.eks-k8s"

exec docker run -it --rm --read-only \
	--hostname ${hostname} -u uws \
	--workdir /home/uws \
	-e HOME=/home/uws \
	-e USER=uws \
	-e UWS_CLUSTER=${uws_cluster} \
	-e AWS_PROFILE=${AWS_PROFILE} \
	-e AWS_REGION=${AWS_REGION} \
	-e K8S_VERSION=${K8S_VERSION} \
	-v ${awsdir}:/home/uws/.aws:ro \
	uws/eks-k8s-2305 /bin/bash -il
