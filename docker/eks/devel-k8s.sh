#!/bin/sh
set -eu

uws_cluster=uwsdev
#~ uws_cluster=${1:?'cluster?'}
#~ shift

eksenv=${PWD}/eks/env/${uws_cluster}.env
awsdir=${PWD}/secret/eks/aws/admin/${uws_cluster}

kubedir=${PWD}/secret/eks/kube/cluster/${uws_cluster}
mkdir -vp ${kubedir}

. ${eksenv}

hostname="${UWS_CLUSTER}.${AWS_REGION}.eks-k8s"

exec docker run -it --rm --read-only \
	--hostname ${hostname} -u uws \
	--workdir /home/uws \
	-e HOME=/home/uws \
	-e USER=uws \
	-e UWS_CLUSTER=${UWS_CLUSTER} \
	-e AWS_PROFILE=${AWS_PROFILE} \
	-e K8S_VERSION=${K8S_VERSION} \
	-v ${awsdir}:/home/uws/.aws:ro \
	-v ${kubedir}:/home/uws/.kube/eksctl/clusters:ro \
	uws/eks-k8s /bin/bash -il
