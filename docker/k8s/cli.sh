#!/bin/sh
set -eu

cluster=${1:?'cluster env?'}
shift

docker_args=${DOCKER_ARGS:-''}

k8s=${PWD}/k8s
pod=${PWD}/pod
awsdir=${PWD}/secret/eks/aws/client/${cluster}
secret=${PWD}/secret/eks/files

eksenv=${PWD}/eks/env/${cluster}.env
# shellcheck disable=SC1090
. ${eksenv}

hostname="${UWS_CLUSTER}.${AWS_REGION}.k8scli"

kubedir=${PWD}/secret/eks/kube/cluster/${cluster}
mkdir -p ${kubedir}

kube_cache=${HOME}/.uwscli/kube/cache/${cluster}
mkdir -p ${kube_cache}
chmod 1777 ${kube_cache}

exec docker run --rm ${docker_args} \
	--hostname ${hostname} -u uws \
	-v ${k8s}:/home/uws/k8s:ro \
	-v ${pod}:/home/uws/pod:ro \
	-v ${awsdir}:/home/uws/.aws:ro \
	-v ${secret}/meteor:/home/uws/secret/meteor:ro \
	-v ${kubedir}:/home/uws/.kube/eksctl/clusters:ro \
	-v ${kube_cache}/:/home/uws/.kube/cache \
	--env-file ${eksenv} \
	uws/${K8S_IMAGE}-2211 "$@"
