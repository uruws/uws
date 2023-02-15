#!/bin/sh
set -eu

# https://docs.aws.amazon.com/eks/latest/userguide/efs-csi.html

fsname=${1:?'fs name?'}

aws efs create-mount-target \
	--region "${AWS_REGION}" \
	--file-system-id "${file_system_id}" \
	--subnet-id "${subnet_id}" \
	--security-groups "${security_group_id}" \
	--tags "\"Key\":\"uwseks-efs\",\"Value\":\"${fsname}\" \"Key\":\"uwseks-efs-cluster\",\"Value\":\"${UWS_CLUSTER}\""

exit 0
