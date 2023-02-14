#!/bin/sh
set -eu

# https://docs.aws.amazon.com/eks/latest/userguide/efs-csi.html

fsname=${1:?'fs name?'}

aws efs create-file-system \
	--output text \
	--region "${AWS_REGION}" \
	--performance-mode generalPurpose \
	--query FileSystemId \
	--encrypted \
	--creation-token "uwseks-efs-${UWS_CLUSTER}-${fsname}" \
	--tags "\"Key\":\"uwseks-efs\",\"Value\":\"${fsname}\" \"Key\":\"uwseks-efs-cluster\",\"Value\":\"${UWS_CLUSTER}\""

exit 0
