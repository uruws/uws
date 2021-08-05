#!/bin/sh
set -eu

uws_cluster=${1:?'cluster?'}
shift

client_mode='false'
if test 'X--client' = "X${1:-'NONE'}"; then
	client_mode='true'
	shift
fi

awsdir=${PWD}/secret/eks/aws
kubedir=${PWD}/secret/eks/kube
secret=${PWD}/secret/eks/files
cadir=${PWD}/secret/ca
files=${PWD}/docker/eks/files
utils=${PWD}/docker/eks/utils
k8s=${PWD}/k8s
pod=${PWD}/pod
cluster=${PWD}/cluster
eksenv=${PWD}/eks/env/${uws_cluster}.env

tmpdir=${PWD}/tmp
mkdir -vp ${tmpdir}

. ${eksenv}

cluster_perms='rw'
hostname="${UWS_CLUSTER}.${AWS_REGION}.eks"
if test 'Xtrue' = "X${client_mode}"; then
	cluster_perms='ro'
	awsdir=${awsdir}/client
	hostname="${hostname}cli"
fi

exec docker run -it --rm \
	--hostname ${hostname} -u uws \
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
	-v ${cadir}:/home/uws/ca:ro \
	-v ${awsdir}:/home/uws/.aws:ro \
	-v ${kubedir}/clusters:/home/uws/.kube/eksctl/clusters:${cluster_perms} \
	-v ${tmpdir}:/home/uws/tmp \
	--env-file ${eksenv} \
	uws/eks $@
