#!/bin/sh
set -eu
for fn in ./secret/aws.env/*/config; do
	ef=$(basename "$(dirname "${fn}")")
	./eks/secrets/aws.env-update.py "${ef}"
done
exit 0
