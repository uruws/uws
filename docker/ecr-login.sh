#!/bin/sh
set -eu
aws=./docker/awscli/run.sh

${aws} ecr get-login-password --region us-east-1 |
	docker login --username AWS --password-stdin 789470191893.dkr.ecr.us-east-1.amazonaws.com

exit 0
