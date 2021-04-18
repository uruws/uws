#!/bin/sh
set -eu
awsdir=${PWD}/secret/eks/aws
kubedir=${PWD}/secret/eks/kube
utils=${PWD}/docker/eks/utils
files=${PWD}/secret/eks/files
exec docker run -it --rm \
	--hostname eks-devel.uws.local -u uws \
	-p 127.0.0.1:8001:8001 \
	-v ${utils}:/home/uws/bin:ro \
	-v ${files}:/home/uws/files:ro \
	-v ${awsdir}:/home/uws/.aws:ro \
	-v ${kubedir}/clusters:/home/uws/.kube/eksctl/clusters \
	uws/eks $@
