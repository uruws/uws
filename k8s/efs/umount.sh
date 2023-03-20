#!/bin/sh
set -eu

# https://docs.aws.amazon.com/eks/latest/userguide/efs-csi.html

fsns=${1:?'fs namespace?'}
fsname=${2:?'fs name?'}

fsid=$(./k8s/efs/getcfg.sh "${fsns}-${fsname}")

mount_targets() (
	aws efs describe-mount-targets \
		--region "${AWS_REGION}" \
		--file-system-id "${fsid}" \
		--query 'MountTargets[*].{f: MountTargetId}' \
		--output text
)

echo "efs umount: ${fsns}/${fsname} (${fsid})"

for mtid in $(mount_targets | uniq); do
	echo "    ${mtid}"
	aws efs delete-mount-target \
		--region "${AWS_REGION}" \
		--mount-target-id "${mtid}" \
		--output text
done

exit 0
