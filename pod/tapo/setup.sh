#!/bin/sh
set -eu
uwskube create namespace "${TAPO_NAMESPACE}"
if test 'X' != "X${TAPO_WORKER_NAMESPACE}"; then
	uwskube create namespace "${TAPO_WORKER_NAMESPACE}"
fi
exit 0
