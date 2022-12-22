#!/bin/sh
set -eu
region=${1:?'region?'}
exec aws events put-targets \
	--region "${region}" \
	--rule GuardDutyEmail \
	--targets 'Id=GuardDutyEmail',"Arn=arn:aws:sns:${region}:${AWS_ACCOUNT_ID}:GuardDutyEmail",'InputTransformer={InputPathsMap={severity="$.detail.severity",Account_ID= "$.detail.accountId",Finding_ID="$.detail.id",Finding_Type="$.detail.type",region="$.region",Finding_description="$.detail.description"},InputTemplate="<Account_ID> <region> <severity> <Finding_Type> <Finding_ID> <Finding_description>"}'
