#!/bin/sh
set -eu

# https://docs.aws.amazon.com/eks/latest/userguide/efs-csi.html

# shellcheck source=/home/uws/secret/secret.env
. ~/secret/secret.env

# IAM policy and role

aws iam create-policy \
	--policy-name AmazonEKS_EFS_CSI_Driver \
	--policy-document "file://${HOME}/k8s/efs/iam-policy.json" \
	--output text

uwseks create iamserviceaccount \
	--namespace kube-system \
	--name efs-csi-controller-sa \
	--attach-policy-arn "arn:aws:iam::${AWS_ACCOUNT_ID}:policy/AmazonEKS_EFS_CSI_Driver" \
	--region "${AWS_REGION}" \
	--approve

# vpc security group

vpc_id=$(aws eks describe-cluster \
	--region "${AWS_REGION}" \
	--name "${UWS_CLUSTER}" \
	--query cluster.resourcesVpcConfig.vpcId \
	--output text)

cidr_range=$(aws ec2 describe-vpcs \
	--region "${AWS_REGION}" \
	--vpc-ids "${vpc_id}" \
	--query 'Vpcs[].CidrBlock' \
	--output text)

security_group_id=$(aws ec2 create-security-group \
	--region "${AWS_REGION}" \
	--group-name EFSSecurityGroup \
	--description "EFS security group" \
	--vpc-id "${vpc_id}" \
	--output text)

aws ec2 authorize-security-group-ingress \
	--region "${AWS_REGION}" \
	--group-id "${security_group_id}" \
	--protocol tcp \
	--port 2049 \
	--cidr "${cidr_range}" \
	--output text

echo "VPC:${vpc_id} CIDR:${cidr_range} SG:${security_group_id}"
~/k8s/efs/setcfg.sh vpc_id "${vpc_id}"
~/k8s/efs/setcfg.sh cidr_range "${cidr_range}"
~/k8s/efs/setcfg.sh security_group_id "${security_group_id}"

exec ~/k8s/efs/install.sh
