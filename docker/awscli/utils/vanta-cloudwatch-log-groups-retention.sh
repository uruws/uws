#!/bin/sh
set -eu

lg_list() (
	cloudwatch-log-groups.sh "${1}" | awk '{ print $4 }'
)

for region in ${VANTA_REGIONS}; do
	echo "--- ${region}"
	for loggroup in `lg_list "${region}"`; do
		echo "---   ${loggroup}"
		cloudwatch-log-groups-retention.sh "${region}" "${loggroup}"
	done
done

exit 0
