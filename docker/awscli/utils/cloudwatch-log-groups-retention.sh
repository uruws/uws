#!/bin/sh
set -eu
region=${1:?'region?'}
loggroup=${2:?'log group name?'}
days=${3:-400}
exec aws logs put-retention-policy \
	--region "${region}" \
	--log-group-name "${loggroup}" \
	--retention-in-days "${days}"
