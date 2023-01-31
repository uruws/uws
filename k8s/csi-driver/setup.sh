#!/bin/sh
set -eu

# https://docs.aws.amazon.com/eks/latest/userguide/ebs-csi.html

# shellcheck source=/home/uws/secret/secret.env
. ~/secret/secret.env

# https://docs.aws.amazon.com/eks/latest/userguide/csi-iam-role.html
uwseks create iamserviceaccount \
	--name ebs-csi-controller-sa \
	--namespace kube-system \
	--attach-policy-arn arn:aws:iam::aws:policy/service-role/AmazonEBSCSIDriverPolicy \
	--approve \
	--role-only \
	--role-name AmazonEKS_EBS_CSI_DriverRole

sleep 1

uwseks create addon --name aws-ebs-csi-driver \
	--service-account-role-arn "arn:aws:iam::${AWS_ACCOUNT_ID}:role/AmazonEKS_EBS_CSI_DriverRole" \
	--force

exit 0
