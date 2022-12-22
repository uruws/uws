#!/bin/sh
set -eu
region=${1:?'region?'}
exec aws events put-targets \
	--region "${region}" \
	--rule GuardDutyEmail \
	--targets 'Id=GuardDutyEmail',"Arn=arn:aws:sns:${region}:${AWS_ACCOUNT_ID}:GuardDutyEmail"
