#!/bin/sh
set -eu

# https://docs.aws.amazon.com/eks/latest/userguide/efs-csi.html

# shellcheck source=/home/uws/secret/secret.env
. ~/secret/secret.env

# IAM policy and role

aws iam create-policy \
	--policy-name AmazonEKS_EFS_CSI_Driver \
	--policy-document ~/k8s/efs/iam-policy.json

uwseks create iamserviceaccount \
	--namespace kube-system \
	--name efs-csi-controller-sa \
	--attach-policy-arn "arn:aws:iam::${AWS_ACCOUNT_ID}:policy/AmazonEKS_EFS_CSI_Driver" \
	--region "${AWS_REGION}" \
	--approve

exec ~/k8s/efs/install.sh
