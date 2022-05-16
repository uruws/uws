#!/bin/sh
set -eu

list_vpc() (
	aws ec2 describe-vpcs --filter Name=state,Values=available --region "${1}" |
		grep -E '^VPCS' |
		awk '{ print $8 }'
)

describe_logs=/tmp/vanta-vpc-flow-logs.describe
describe_logs_group=/tmp/vanta-vpc-flow-logs-group.describe

for region in ${VANTA_REGIONS}; do
	aws logs describe-log-groups --region "${region}" >${describe_logs_group}
	if ! grep -qF vpc-flow-logs ${describe_logs_group}; then
		~/bin/vpc-flow-logs-group.sh "${region}"
	fi
	aws ec2 describe-flow-logs --region "${region}" >${describe_logs}
	for vpc in $(list_vpc "${region}"); do
		echo "*** ${region} -> ${vpc}"
		if grep -qF "${vpc}" ${describe_logs}; then
			echo "done already!"
		else
			~/bin/vpc-flow-logs.sh "${region}" "${vpc}"
		fi
	done
done

exit 0
