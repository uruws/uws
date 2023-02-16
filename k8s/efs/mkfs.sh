#!/bin/sh
set -eu

# https://docs.aws.amazon.com/eks/latest/userguide/efs-csi.html

fsns=${1:?'fs namespace?'}
fsname=${2:?'fs name?'}

fsid=$(aws efs create-file-system \
	--output text \
	--query FileSystemId \
	--region "${AWS_REGION}" \
	--performance-mode generalPurpose \
	--encrypted \
	--creation-token "uwseks-efs-${UWS_CLUSTER}-${fsns}-${fsname}" \
	--tags "Key=uwseks-efs-${UWS_CLUSTER},Value=\"${fsns}/${fsname}\"")

echo "${fsns}/${fsname} created: ${fsid}"
~/k8s/efs/setcfg.sh "${fsns}-${fsname}" "${fsid}"

UWSEFS_NAME="${fsname}"
export UWSEFS_NAME

UWSEFS_FSID="${fsid}"
export UWSEFS_FSID

envsubst <~/k8s/efs/storageclass.yaml | uwskube apply -n "${fsns}" -f -

exit 0
