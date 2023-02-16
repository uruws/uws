#!/bin/sh
set -eu

# https://docs.aws.amazon.com/eks/latest/userguide/efs-csi.html

fsname=${1:?'fs name?'}

fs_id=$(./k8s/efs/getcfg.sh "fs-${fsname}")

mount_targets() (
	aws efs describe-mount-targets \
		--region "${AWS_REGION}" \
		--file-system-id "${fs_id}" \
		--query 'MountTargets[*].{f: MountTargetId}' \
		--output text
)

echo "efs umount: ${fsname} (${fs_id})"

for mtid in $(mount_targets | uniq); do
	echo "    ${mtid}"
	aws efs delete-mount-target \
		--region "${AWS_REGION}" \
		--mount-target-id "${mtid}" \
		--output text
done

exit 0
