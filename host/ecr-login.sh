#!/bin/sh
set -eu

AWS_REGION=${1:-'us-east-1'}

echo "i - ECR login aws region: ${AWS_REGION}"
aws ecr get-login-password --region ${AWS_REGION} |
	docker login --username AWS --password-stdin 789470191893.dkr.ecr.${region}.amazonaws.com

exit 0
