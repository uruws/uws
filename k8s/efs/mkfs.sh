#!/bin/sh
set -eu

# https://docs.aws.amazon.com/eks/latest/userguide/efs-csi.html

fsns=${1:?'fs namespace?'}
fsname=${2:?'fs name?'}

UWSEFS_NAME="${fsns}-${fsname}"
export UWSEFS_NAME

fsid=$(aws efs create-file-system \
	--output text \
	--query FileSystemId \
	--region "${AWS_REGION}" \
	--performance-mode generalPurpose \
	--encrypted \
	--creation-token "uwseks-efs-${UWS_CLUSTER}-${fsns}-${fsname}" \
	--tags "Key=uwseks-efs-${UWS_CLUSTER},Value=\"${UWSEFS_NAME}\"")

UWSEFS_FSID="${fsid}"
export UWSEFS_FSID

echo "${UWSEFS_NAME} created: ${UWSEFS_FSID}"

~/k8s/efs/setcfg.sh "${UWSEFS_NAME}" "${UWSEFS_FSID}"

envsubst <~/k8s/efs/storageclass.yaml | uwskube apply -f -

exit 0
