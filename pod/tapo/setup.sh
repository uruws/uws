#!/bin/sh
set -eu
uwskube create namespace "${TAPO_NAMESPACE}"
uwskube create namespace "${TAPO_API_NAMESPACE}" || true
uwskube create namespace "${TAPO_CDN_NAMESPACE}" || true
if test 'X' != "X${TAPO_WORKER_NAMESPACE}"; then
	uwskube create namespace "${TAPO_WORKER_NAMESPACE}"
fi
exit 0
