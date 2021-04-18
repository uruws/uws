#!/bin/sh
set -eu
awsdir=${PWD}/secret/eks/aws
kubedir=${PWD}/secret/eks/kube
files=${PWD}/secret/eks/files
utils=${PWD}/docker/eks/utils
k8s=${PWD}/k8s
cluster=${PWD}/cluster
exec docker run -it --rm \
	--hostname eks-devel.uws.local -u uws \
	-p 127.0.0.1:8001:8001 \
	-p 127.0.0.1:9090:9090 \
	-p 127.0.0.1:9091:9091 \
	-p 127.0.0.1:9093:9093 \
	-v ${utils}:/home/uws/bin:ro \
	-v ${k8s}:/home/uws/k8s:ro \
	-v ${cluster}:/home/uws/cluster:ro \
	-v ${files}:/home/uws/files:ro \
	-v ${awsdir}:/home/uws/.aws:ro \
	-v ${kubedir}/clusters:/home/uws/.kube/eksctl/clusters \
	uws/eks $@
