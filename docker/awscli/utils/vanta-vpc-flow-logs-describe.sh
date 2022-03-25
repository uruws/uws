#!/bin/sh
set -eu

for region in ${VANTA_REGIONS}; do
	aws logs describe-log-groups --region "${region}" \
		--log-group-name-prefix vpc-flow-logs
	aws ec2 describe-flow-logs --region "${region}" \
		--filter Name=log-group-name,Values=vpc-flow-logs
done

exit 0
