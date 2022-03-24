#!/bin/sh
set -eu

list_vpc() (
	aws ec2 describe-vpcs --filter Name=state,Values=available --region ${1} |
		grep -E '^VPCS' |
		awk '{ print $8 }'
)

describe_logs=/tmp/vanta-vpc-flow-logs.describe

for region in ${VANTA_REGIONS}; do
	aws ec2 describe-flow-logs --region "${region}" >${describe_logs}
	for vpc in $(list_vpc ${region}); do
		echo "*** ${region} -> ${vpc}"
		if grep -qF "${vpc}" ${describe_logs}; then
			echo "done already!"
		else
			~/bin/vpc-flow-logs.sh "${region}" "${vpc}"
		fi
	done
done

exit 0
