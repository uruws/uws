#!/bin/sh
set -eu
exec aws ec2 create-flow-logs --resource-type VPC \
	--resource-ids ${vpcid} \
	--traffic-type REJECT \
	--log-group-name vpc-flow-logs \
	--deliver-logs-permission-arn ${AWS_CLOUDWATCH_ARN}
