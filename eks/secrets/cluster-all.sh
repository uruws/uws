#!/bin/sh
set -eu
for ef in ./eks/env/*.env; do
	./eks/secrets/cluster-update.sh "${ef}"
done
exit 0
