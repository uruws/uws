#!/bin/sh
set -eu

cluster=${1:?'cluster name?'}
prof=${2:?'profile?'}
region=${3:?'region?'}

admin_dir=${PWD}/secret/eks/aws/admin/${cluster}
client_dir=${PWD}/secret/eks/aws/client/${cluster}
cluster_dir=${PWD}/cluster/${cluster}
kubedir=${PWD}/secret/eks/kube/cluster/${cluster}
eksenv=${PWD}/eks/env/${cluster}.env
secret=${PWD}/secret/eks/files
sshdir=${secret}/ssh/${cluster}

install -v -d -m 0750 "${admin_dir}"
install -v -d -m 0750 "${client_dir}"
install -v -d -m 0750 "${cluster_dir}"
install -v -d -m 0750 "${kubedir}"
install -v -d -m 0750 "${sshdir}"

touch "${admin_dir}/config"
touch "${client_dir}/config"

{
	echo '[default]'
	echo "region = ${region}"
	echo ''
	echo "[${prof}]"
	echo "region = ${region}"
} >"${admin_dir}/config"

cat "${admin_dir}/config" >"${client_dir}/config"

k8s_version=$(cat "${PWD}/docker/k8s/VERSION")
k8s_tag=$(cat "${PWD}/docker/k8s/TAG")

{
	echo "UWS_CLUSTER=${cluster}"
	echo "CLUSTER_HOST=${cluster}"
	echo ''
	echo "AWS_PROFILE=${prof}"
	echo "AWS_REGION=${region}"
	echo "AWS_ZONES=${region}a,${region}b,${region}c"
	echo ''
	echo "K8S_VERSION=${k8s_version}"
	echo "K8S_IMAGE=k8s-${k8s_tag}"
	echo "EKS_IMAGE=eks-${k8s_tag}"
	echo ''
	echo 'AWS_INSTANCE_TYPES=c5n.large,c5.large,c5a.large'
	echo 'AWS_SPOT_INSTANCE=true'
} >"${eksenv}"

./secret/eks/files/ssh/gen.sh "${cluster}"

touch "${admin_dir}/credentials"
touch "${client_dir}/credentials"

exec ./eks/secrets/cluster.py --profile "${prof}" "${cluster}"
