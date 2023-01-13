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

git rm -r ${admin_dir}
git rm -r ${client_dir}
git rm -r ${cluster_dir}
git rm -r ${kubedir}
git rm -r ${sshdir}

git rm -r ${eksenv}

exit 0
