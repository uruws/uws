#!/bin/sh
set -eu
if test 'X' = "X${TAPO_WORKER_NAMESPACE}"; then
	exit 0
fi
exec ~/pod/tapo/events.sh "${TAPO_WORKER_NAMESPACE}" "$@"
