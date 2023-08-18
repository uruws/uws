#!/bin/sh
set -eu
replicas=${1:?'app replicas?'}
if test 'X' = "X${TAPO_WORKER_NAMESPACE}"; then
	exit 0
fi
exec ~/pod/tapo/scale.sh "${TAPO_WORKER_NAMESPACE}" worker "${replicas}"
