#!/bin/sh
set -eu

uws_cluster=${1:?'cluster?'}
shift

client_mode='false'
if test 'X--client' = "X${1:-'NONE'}"; then
	client_mode='true'
	shift
fi

awsdir=${PWD}/secret/eks/aws/admin/${uws_cluster}
secret=${PWD}/secret/eks/files
cadir=${PWD}/secret/ca
utils=${PWD}/docker/eks/utils
ekslib=${PWD}/eks/lib
k8s=${PWD}/k8s
pod=${PWD}/pod
eksenv=${PWD}/eks/env/${uws_cluster}.env

tmpdir=${PWD}/tmp
mkdir -vp "${tmpdir}"

kubedir=${PWD}/secret/eks/kube/cluster/${uws_cluster}
mkdir -vp "${kubedir}"

kubecfg=${kubedir}/${uws_cluster}
if test -s "${kubecfg}"; then
	chmod 0600 "${kubecfg}"
fi

cluster=${PWD}/cluster/${uws_cluster}
mkdir -vp "${cluster}"

# shellcheck disable=SC1090
. ${eksenv}

cluster_perms='rw'
hostname="${uws_cluster}.${AWS_REGION}.eks"
if test 'Xtrue' = "X${client_mode}"; then
	cluster_perms='ro'
	awsdir=${PWD}/secret/eks/aws/client/${uws_cluster}
	hostname="${hostname}cli"
fi

if ! test -s "${awsdir}/config"; then
	echo "${awsdir}/config: file not found" >&2
	exit 3
fi
if ! test -s "${awsdir}/credentials"; then
	echo "${awsdir}/credentials: file not found" >&2
	exit 3
fi

if ! test -s "${secret}/ssh/${uws_cluster}/node.pub"; then
	echo "${secret}/ssh/${uws_cluster}/node.pub: file not found" >&2
	exit 4
fi

docker_args="-it --rm"
if test "X${UWSEKSCMD:-NONE}" = 'true'; then
	docker_args="--rm"
fi

install -v -d -m 0750 "${ekslib}/__pycache__"

exec docker run ${docker_args} \
	--hostname "${hostname}" -u uws \
	-p 127.0.0.1:0:3000 \
	-p 127.0.0.1:0:8001 \
	-p 127.0.0.1:0:9090 \
	-p 127.0.0.1:0:9091 \
	-p 127.0.0.1:0:9093 \
	-p 127.0.0.1:0:8899 \
	-e PYTHONPATH=/home/uws/lib \
	-v "${utils}:/home/uws/bin:ro" \
	-v "${ekslib}:/home/uws/lib:ro" \
	-v "${ekslib}/__pycache__:/home/uws/lib/__pycache__:rw" \
	-v "${k8s}:/home/uws/k8s:ro" \
	-v "${pod}:/home/uws/pod:ro" \
	-v "${cluster}:/home/uws/cluster:ro" \
	-v "${secret}:/home/uws/secret:ro" \
	-v "${cadir}:/home/uws/ca:ro" \
	-v "${awsdir}:/home/uws/.aws:ro" \
	-v "${kubedir}:/home/uws/.kube/eksctl/clusters:${cluster_perms}" \
	-v "${tmpdir}:/home/uws/tmp" \
	--env-file "${eksenv}" \
	"uws/${EKS_IMAGE}-2305" "$@"
