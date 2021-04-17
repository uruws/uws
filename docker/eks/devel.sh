#!/bin/sh
set -eu
awsdir=${HOME}/.uws/eks/aws
kubedir=${HOME}/.uws/eks/kube
mkdir -vp ${awsdir} ${kubedir}
utils=${PWD}/docker/eks/utils
test -d ${utils} || {
	echo "${utils}: directory not found" >&2
	exit 1
}
exec docker run -it --rm --name uws-eks-devel \
	--hostname eks-devel.uws.local -u uws \
	-v ${utils}:/home/uws/bin:ro \
	-v ${awsdir}:/home/uws/.aws:ro \
	-v ${kubedir}:/home/uws/.kube \
	uws/eks $@
