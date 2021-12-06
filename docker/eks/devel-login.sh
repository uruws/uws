#!/bin/sh
set -eu

utils=${PWD}/docker/eks/utils

install -v -d -m 0750 ${PWD}/tmp/eks

exec docker run -it --rm --name eks-devel \
	--hostname eks-devel.uws.local -u uws \
	-v ${utils}:/home/uws/bin:ro \
	-v ${PWD}/cluster:/home/uws/cluster:ro \
	-v ${PWD}/eks:/home/uws/eks:ro \
	-v ${PWD}/secret/eks/files:/home/uws/secret:ro \
	-v ${PWD}/tmp/eks:/home/uws/tmp \
	uws/eks:devel $@
