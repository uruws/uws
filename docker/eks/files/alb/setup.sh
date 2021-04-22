#!/bin/sh
set -eu

. ~/bin/env.export

cluster=${UWS_CLUSTER}
helm="helm --kubeconfig ~/.kube/eksctl/clusters/${cluster}"
files=~/files
secret=~/secret

. ${secret}/secret.env

aws iam create-policy \
	--policy-name uwseks-${cluster}-AWSLoadBalancerControllerIAMPolicy \
	--policy-document file://${files}/alb-iam-policy.json

uwseks create iamserviceaccount \
	--namespace=kube-system \
	--name=alb-controller \
	--attach-policy-arn=arn:aws:iam::${AWS_ACCOUNT_ID}:policy/uwseks-${cluster}-AWSLoadBalancerControllerIAMPolicy \
	--override-existing-serviceaccounts \
	--approve

${helm} repo add eks https://aws.github.io/eks-charts
${helm} repo update

uwskube apply -k \
	"github.com/aws/eks-charts/stable/aws-load-balancer-controller//crds?ref=master"

${helm} upgrade -i alb-controller eks/aws-load-balancer-controller \
	-n kube-system \
	--set clusterName=${cluster} \
	--set serviceAccount.create=false \
	--set serviceAccount.name=alb-controller

exit 0
