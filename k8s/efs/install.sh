#!/bin/sh
set -eu

# https://docs.aws.amazon.com/eks/latest/userguide/efs-csi.html

helm upgrade -i aws-efs-csi-driver aws-efs-csi-driver/aws-efs-csi-driver \
	--repo https://kubernetes-sigs.github.io/aws-efs-csi-driver/ \
	--namespace kube-system \
	--set "image.repository=602401143452.dkr.ecr.${AWS_REGION}.amazonaws.com/eks/aws-efs-csi-driver" \
	--set controller.serviceAccount.create=false \
	--set controller.serviceAccount.name=efs-csi-controller-sa

exit 0
