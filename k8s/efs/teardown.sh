#!/bin/sh
set -u

# shellcheck source=/home/uws/secret/secret.env
. ~/secret/secret.env

~/k8s/efs/uninstall.sh

aws ec2 delete-security-group \
	--region "${AWS_REGION}" \
	--group-id "${security_group_id}" \
	--output text

uwseks delete iamserviceaccount --wait --approve \
	--namespace kube-system \
	--name efs-csi-controller-sa

aws iam delete-policy \
	--policy-arn "arn:aws:iam::${AWS_ACCOUNT_ID}:policy/AmazonEKS_EFS_CSI_Driver"

exit 0
