#!/bin/sh
set -u

# shellcheck source=/home/uws/secret/secret.env
. ~/secret/secret.env

~/k8s/efs/uninstall.sh

security_group_id=$(~/k8s/efs/getcfg.sh security-group-id)

aws ec2 delete-security-group \
	--region "${AWS_REGION}" \
	--group-id "${security_group_id}" \
	--output text

uwseks delete iamserviceaccount --wait \
	--namespace kube-system \
	--name efs-csi-controller-sa

aws iam delete-policy \
	--policy-arn "arn:aws:iam::${AWS_ACCOUNT_ID}:policy/AmazonEKS_EFS_CSI_Driver"

~/k8s/efs/delcfg.sh vpc-id
~/k8s/efs/delcfg.sh cidr-range
~/k8s/efs/delcfg.sh security-group-id

exit 0
