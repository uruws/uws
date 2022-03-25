#!/bin/sh
set -eu
region=${1:?'region?'}
flow_logs=${2:?'flow-log-ids?'}
exec aws ec2 delete-flow-logs \
	--region "${region}" \
	--flow-log-ids "${flow_logs}"
