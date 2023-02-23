#!/bin/sh
set -u

# shellcheck disable=SC1090 disable=SC1091
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

~/k8s/efs/delcfg.sh vpc-id
~/k8s/efs/delcfg.sh cidr-range
~/k8s/efs/delcfg.sh security-group-id

exit 0
