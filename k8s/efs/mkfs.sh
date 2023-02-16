#!/bin/sh
set -eu

# https://docs.aws.amazon.com/eks/latest/userguide/efs-csi.html

fsname=${1:?'fs name?'}

fsid=$(aws efs create-file-system \
	--output text \
	--query FileSystemId \
	--region "${AWS_REGION}" \
	--performance-mode generalPurpose \
	--encrypted \
	--creation-token "uwseks-efs-${UWS_CLUSTER}-${fsname}" \
	--tags "\"Key\"=\"uwseks-efs\",\"Value\"=\"${fsname}\" \"Key\"=\"uwseks-efs-cluster\",\"Value\"=\"${UWS_CLUSTER}\"")

echo "${fsname} created: ${fsid}"
~/k8s/efs/setcfg.sh "fs-${fsname}" "${fsid}"

exit 0
