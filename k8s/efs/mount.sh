#!/bin/sh
set -eu

# https://docs.aws.amazon.com/eks/latest/userguide/efs-csi.html

fsname=${1:?'fs name?'}

vpc_id=$(./k8s/efs/getcfg.sh vpc-id)
secgroup_id=$(./k8s/efs/getcfg.sh security-group-id)
fs_id=$(./k8s/efs/getcfg.sh "fs-${fsname}")

subnets() (
	aws ec2 describe-subnets \
		--output text \
		--region "${AWS_REGION}" \
		--filters "Name=vpc-id,Values=${vpc_id}" \
		--query 'Subnets[*].{SubnetId: SubnetId}'
)

echo "efs mount: ${fsname} (${fsid})"

for sn in $(subnets); do
	echo "  ${sn}"
	aws efs create-mount-target \
		--output text \
		--region "${AWS_REGION}" \
		--file-system-id "${fs_id}" \
		--subnet-id "${sn}" \
		--security-groups "${secgroup_id}"
done

exit 0
