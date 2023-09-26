#!/bin/sh
set -eu
if test 'X' = "X${TAPO_WORKER_NAMESPACE}"; then
	exit 0
fi
exec ~/pod/lib/watch.py -n "${TAPO_WORKER_NAMESPACE}"
