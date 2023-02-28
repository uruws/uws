#!/bin/sh
set -eu

# https://docs.aws.amazon.com/eks/latest/userguide/efs-csi.html

# IAM policy

aws iam create-policy \
	--policy-name AmazonEKS_EFS_CSI_Driver \
	--policy-document "file://${HOME}/k8s/efs/iam-policy.json" \
	--output text

exit 0
