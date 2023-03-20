#!/bin/sh
set -eu

# https://docs.aws.amazon.com/eks/latest/userguide/efs-csi.html

fsns=${1:?'fs namespace?'}
fsname=${2:?'fs name?'}

UWSEFS_NAME="${fsns}-${fsname}"

fsid=$(./k8s/efs/getcfg.sh "${UWSEFS_NAME}")

exec aws efs describe-mount-targets \
	--output table \
	--region "${AWS_REGION}" \
	--file-system-id "${fsid}" \
	--query 'MountTargets[*].{AZ: AvailabilityZoneName, Id: MountTargetId, Status: LifeCycleState}'
