#!/bin/sh
set -eu

utils=${PWD}/docker/eks/utils
ekslib=${PWD}/eks/lib

install -v -d -m 0750 ${PWD}/tmp/eks
install -v -d -m 0750 ${ekslib}/__pycache__

exec docker run --rm --name eks-devel \
	--hostname eks-devel.uws.local -u uws \
	-e PYTHONPATH=/home/uws/lib \
	-v ${utils}:/home/uws/bin:ro \
	-v ${ekslib}:/home/uws/lib:ro \
	-v ${ekslib}/__pycache__:/home/uws/lib/__pycache__:rw \
	-v ${PWD}/cluster:/home/uws/cluster:ro \
	-v ${PWD}/eks:/home/uws/eks:ro \
	-v ${PWD}/secret/eks/files:/home/uws/secret:ro \
	-v ${PWD}/tmp/eks:/home/uws/tmp \
	uws/eks:devel "$@"
