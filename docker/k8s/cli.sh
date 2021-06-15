#!/bin/sh
set -eu

eksenv=${1:?'cluster env?'}
shift
. ./eks/env/${eksenv}.env

k8s=${PWD}/k8s
pod=${PWD}/pod
awsdir=${PWD}/secret/eks/aws/client
kubedir=${PWD}/secret/eks/kube

hostname="${UWS_CLUSTER}.${AWS_REGION}.k8scli"

exec docker run -it --rm \
	--hostname ${hostname} -u uws \
	-v ${k8s}:/home/uws/k8s:ro \
	-v ${pod}:/home/uws/pod:ro \
	-v ${awsdir}:/home/uws/.aws:ro \
	-v ${kubedir}/clusters:/home/uws/.kube/eksctl/clusters:ro \
	-e UWS_CLUSTER=${UWS_CLUSTER} \
	-e AWS_PROFILE=${AWS_PROFILE} \
	-e AWS_REGION=${AWS_REGION} \
	uws/k8s $@
