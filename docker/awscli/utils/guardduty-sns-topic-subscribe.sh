#!/bin/sh
set -eu
region=${1:?'region?'}
exec aws sns subscribe \
	--region "${region}" \
	--topic-arn "arn:aws:sns:${region}:${AWS_ACCOUNT_ID}:GuardDutyEmail" \
	--protocol email \
	--notification-endpoint "${GUARDDUTY_NOTIFICATION_ENDPOINT}"
