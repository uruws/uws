#!/bin/sh
set -eu
region=${1:?'region?'}
exec aws logs create-log-group \
	--region "${region}" \
	--log-group-name vpc-flow-logs
