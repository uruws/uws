#!/bin/sh
set -eu

# https://docs.aws.amazon.com/eks/latest/userguide/efs-csi.html

fsns=${1:?'fs namespace?'}
fsname=${2:?'fs name?'}

UWSEFS_NAME="${fsns}-${fsname}"

fsid=$(./k8s/efs/getcfg.sh "${UWSEFS_NAME}")

aws efs delete-file-system \
	--output text \
	--region "${AWS_REGION}" \
	--file-system-id "${fsid}"

~/k8s/efs/delcfg.sh "${UWSEFS_NAME}"

uwskube delete storageclass "efs-${UWSEFS_NAME}"

exit 0
