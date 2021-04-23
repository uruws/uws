#!/bin/sh
set -eu

aws_profile=${AWS_PROFILE:-'uwsdev'}
aws_region=${AWS_REGION:-'us-west-2'}
uws_cluster=${UWS_CLUSTER:-'uwsdev'}

client_mode='false'
if test 'X--client' = "X${1:-'NONE'}"; then
	client_mode='true'
	shift
fi

awsdir=${PWD}/secret/eks/aws
kubedir=${PWD}/secret/eks/kube
secret=${PWD}/secret/eks/files
files=${PWD}/docker/eks/files
utils=${PWD}/docker/eks/utils
k8s=${PWD}/k8s
pod=${PWD}/pod
cluster=${PWD}/cluster

tmpdir=${PWD}/tmp
mkdir -vp ${tmpdir}

cluster_perms='rw'
if test 'Xtrue' = "X${client_mode}"; then
	cluster_perms='ro'
fi

exec docker run -it --rm \
	--hostname eks-devel.uws.local -u uws \
	-p 127.0.0.1:0:3000 \
	-p 127.0.0.1:0:8001 \
	-p 127.0.0.1:0:9090 \
	-p 127.0.0.1:0:9091 \
	-p 127.0.0.1:0:9093 \
	-v ${utils}:/home/uws/bin:ro \
	-v ${k8s}:/home/uws/k8s:ro \
	-v ${pod}:/home/uws/pod:ro \
	-v ${cluster}:/home/uws/cluster:ro \
	-v ${files}:/home/uws/files:ro \
	-v ${secret}:/home/uws/secret:ro \
	-v ${awsdir}:/home/uws/.aws:ro \
	-v ${kubedir}/clusters:/home/uws/.kube/eksctl/clusters:${cluster_perms} \
	-v ${tmpdir}:/home/uws/tmp \
	-e AWS_PROFILE=${aws_profile} \
	-e AWS_REGION=${aws_region} \
	-e UWS_CLUSTER=${uws_cluster} \
	uws/eks $@
