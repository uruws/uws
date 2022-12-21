#!/bin/sh
set -eu

for region in ${VANTA_REGIONS}; do
	echo "--- ${region}"
	guardduty-sns-topic.sh "${region}"
	guardduty-sns-topic-subscribe.sh "${region}"
done

exit 0
