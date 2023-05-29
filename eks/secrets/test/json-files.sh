#!/bin/sh
set -eu

find ./secret -type f -name '*.json' | sort -u | while read -r fn; do
	echo "-- ${fn}"
	python3 -m json.tool "${fn}" /dev/null
done

exit 0
