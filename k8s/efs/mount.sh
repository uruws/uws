#!/bin/sh
set -eu

# https://docs.aws.amazon.com/eks/latest/userguide/efs-csi.html

fsns=${1:?'fs namespace?'}
fsname=${2:?'fs name?'}

UWSEFS_NAME="${fsns}-${fsname}"

vpc_id=$(./k8s/efs/getcfg.sh vpc-id)
secgroup_id=$(./k8s/efs/getcfg.sh security-group-id)
fsid=$(./k8s/efs/getcfg.sh "${UWSEFS_NAME}")

subnets() (
	aws ec2 describe-subnets \
		--output text \
		--region "${AWS_REGION}" \
		--filters "Name=vpc-id,Values=${vpc_id}" \
		--query 'Subnets[*].{SubnetId: SubnetId}'
)

echo "efs mount: ${UWSEFS_NAME} (${fsid})"

for sn in $(subnets | uniq); do
	echo "*** mount target: ${fsid} ${sn}"
	aws efs create-mount-target \
		--output text \
		--region "${AWS_REGION}" \
		--file-system-id "${fsid}" \
		--subnet-id "${sn}" \
		--security-groups "${secgroup_id}"
done

exit 0
