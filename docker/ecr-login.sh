#!/bin/sh
set -eu

region=${1:-'us-east-1'}
aws=./docker/awscli/run.sh

${aws} ecr get-login-password --region ${region} |
	docker login --username AWS --password-stdin 789470191893.dkr.ecr.${region}.amazonaws.com

exit 0
