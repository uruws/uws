#!/bin/sh
set -eu

# https://docs.aws.amazon.com/eks/latest/userguide/efs-csi.html

fsns=${1:?'fs namespace?'}
fsname=${2:?'fs name?'}

fsid=$(./k8s/efs/getcfg.sh "${fsns}-${fsname}")

aws efs delete-file-system \
	--output text \
	--region "${AWS_REGION}" \
	--file-system-id "${fsid}"

~/k8s/efs/delcfg.sh "${fsns}-${fsname}"

uwskube delete storageclass -n "${fsns}" "uwsefs-${fsname}"

exit 0
