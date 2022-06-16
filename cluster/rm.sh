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

rm -vrf ${admin_dir}
rm -vrf ${client_dir}
rm -vrf ${cluster_dir}
rm -vrf ${kubedir}
rm -vrf ${sshdir}

rm -vf ${eksenv}

exit 0
