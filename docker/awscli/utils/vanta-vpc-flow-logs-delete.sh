#!/bin/sh
set -eu

list_fl() (
	aws ec2 describe-flow-logs --region "${1}" \
		--filter Name=log-group-name,Values=vpc-flow-logs |
		grep -E '^FLOWLOGS' |
		awk '{ print $7 }' |
		grep -E '^fl-'
)

for region in ${VANTA_REGIONS}; do
	for fl in $(list_fl ${region}); do
		echo "*** ${region} -> ${fl}"
		~/bin/vpc-flow-logs-delete.sh "${region}" "${fl}"
	done
done

exit 0
