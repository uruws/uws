#!/bin/sh
set -eu

. ~/bin/env.export

cluster=${UWS_CLUSTER}
helm="helm --kubeconfig ~/.kube/eksctl/clusters/${cluster}"
files=~/files
secret=~/secret

. ${secret}/secret.env

${helm} uninstall -n kube-system alb-controller

uwskube delete -k \
	"github.com/aws/eks-charts/stable/aws-load-balancer-controller//crds?ref=master"

uwseks delete iamserviceaccount \
	--namespace=kube-system \
	--name=alb-controller \
	--wait

aws iam delete-policy \
	--policy-arn=arn:aws:iam::${AWS_ACCOUNT_ID}:policy/uwseks-${cluster}-AWSLoadBalancerControllerIAMPolicy

exit 0
