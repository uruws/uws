#!/bin/sh
set -eu

# https://docs.aws.amazon.com/eks/latest/userguide/efs-csi.html

fsname=${1:?'fs name?'}

fs_id=$(./k8s/efs/getcfg.sh "fs-${fsname}")

aws efs delete-file-system \
	--output text \
	--region "${AWS_REGION}" \
	--file-system-id "${fs_id}"

~/k8s/efs/delcfg.sh "fs-${fsname}"

exit 0
