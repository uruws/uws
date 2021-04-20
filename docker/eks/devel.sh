#!/bin/sh
set -eu
awsdir=${PWD}/secret/eks/aws
kubedir=${PWD}/secret/eks/kube
secrets=${PWD}/secret/eks/files
files=${PWD}/docker/eks/files
utils=${PWD}/docker/eks/utils
k8s=${PWD}/k8s
pod=${PWD}/pod
cluster=${PWD}/cluster
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
	-v ${secrets}:/home/uws/secret:ro \
	-v ${awsdir}:/home/uws/.aws:ro \
	-v ${kubedir}/clusters:/home/uws/.kube/eksctl/clusters \
	uws/eks $@
