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

install -v -d -m 0750 ${admin_dir}
install -v -d -m 0750 ${client_dir}
install -v -d -m 0750 ${cluster_dir}
install -v -d -m 0750 ${kubedir}
install -v -d -m 0750 ${sshdir}

touch ${admin_dir}/config
touch ${client_dir}/config

echo '[default]'           >${admin_dir}/config
echo "region = ${region}" >>${admin_dir}/config
echo ''                   >>${admin_dir}/config
echo "[${prof}]"          >>${admin_dir}/config
echo "region = ${region}" >>${admin_dir}/config

cat ${admin_dir}/config >${client_dir}/config

echo "UWS_CLUSTER=${cluster}"                      >${eksenv}
echo "CLUSTER_HOST=${cluster}"                    >>${eksenv}
echo "AWS_PROFILE=${prod}"                        >>${eksenv}
echo "AWS_REGION=${region}"                       >>${eksenv}
echo "AWS_ZONES=${region}a,${region}b,${region}c" >>${eksenv}

./secret/eks/files/ssh/gen.sh "${cluster}"

touch ${admin_dir}/credentials
touch ${client_dir}/credentials

exec ./eks/secrets/cluster.py --profile "${prof}" --region "${region}" "${cluster}"
