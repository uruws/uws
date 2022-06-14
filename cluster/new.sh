#!/bin/sh
set -eu

cluster=${1:?'cluster name?'}

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
touch ${admin_dir}/credentials

touch ${client_dir}/config
touch ${client_dir}/credentials

touch ${eksenv}

./secret/eks/files/ssh/gen.sh "${cluster}"

exit 0
