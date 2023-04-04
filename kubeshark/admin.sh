#!/bin/sh
set -eu

#~ awsdir=${PWD}/secret/eks/aws/admin
awsdir=${PWD}/secret/eks/aws/client
ksdir=${PWD}/kubeshark

tmpdir=${PWD}/tmp/kubeshark
mkdir -vp "${tmpdir}"

kubedir=${PWD}/secret/eks/kube/cluster
mkdir -vp "${kubedir}"

exec docker run -it --rm -u uws\
	--hostname ksadm \
	-p 127.0.0.1:8898:8898 \
	-p 127.0.0.1:8899:8899 \
	-v "${awsdir}:/home/uws/secret/eks/aws/client:ro" \
	-v "${kubedir}:/home/uws/secret/eks/kube/cluster:ro" \
	-v "${ksdir}:/home/uws/kubeshark:ro" \
	-v "${tmpdir}:/home/uws/tmp" \
	uws/k8s-124-2211
