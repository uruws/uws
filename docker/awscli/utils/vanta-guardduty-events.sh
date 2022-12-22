#!/bin/sh
set -eu

for region in ${VANTA_REGIONS}; do
	echo "--- ${region}"
	guardduty-events-rule.sh "${region}"
	guardduty-events-target.sh "${region}"
done

exit 0
