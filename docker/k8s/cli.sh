#!/bin/sh
set -eu

cluster=${1:?'cluster env?'}
shift

k8s=${PWD}/k8s
pod=${PWD}/pod
awsdir=${PWD}/secret/eks/aws/client
kubedir=${PWD}/secret/eks/kube
eksenv=${PWD}/eks/env/${cluster}.env

. ${eksenv}
hostname="${UWS_CLUSTER}.${AWS_REGION}.k8scli"

kube_cache=${HOME}/.uwscli/kube/cache
mkdir -p ${kube_cache}
chmod 1777 ${kube_cache}

exec docker run -it --rm \
	--hostname ${hostname} -u uws \
	-v ${k8s}:/home/uws/k8s:ro \
	-v ${pod}:/home/uws/pod:ro \
	-v ${awsdir}:/home/uws/.aws:ro \
	-v ${kubedir}/clusters:/home/uws/.kube/eksctl/clusters:ro \
	-v ${kube_cache}/:/home/uws/.kube/cache \
	--env-file ${eksenv} \
	uws/k8s $@
