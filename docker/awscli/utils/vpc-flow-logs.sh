#!/bin/sh
set -eu
region=${1:?'region?'}
vpcid=${2:?'vpc-id?'}
exec aws ec2 create-flow-logs --resource-type VPC \
	--resource-ids ${vpcid} \
	--region ${region} \
	--traffic-type REJECT \
	--log-group-name vpc-flow-logs \
	--deliver-logs-permission-arn ${AWS_CLOUDWATCH_ARN}
