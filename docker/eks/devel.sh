#!/bin/sh
set -eu
awsdir=${PWD}/secret/eks/aws
kubedir=${PWD}/secret/eks/kube
utils=${PWD}/docker/eks/utils
files=${PWD}/secret/eks/files
exec docker run -it --rm --name uws-eks-devel \
	--hostname eks-devel.uws.local -u uws \
	-v ${utils}:/home/uws/bin:ro \
	-v ${files}:/home/uws/files:ro \
	-v ${awsdir}:/home/uws/.aws:ro \
	-v ${kubedir}/clusters:/home/uws/.kube/eksctl/clusters \
	uws/eks $@
