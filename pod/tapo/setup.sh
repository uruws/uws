#!/bin/sh
set -eu

uwskube create namespace "${TAPO_NAMESPACE}"

if test "X${TAPO_API_NAMESPACE}" != "X${TAPO_NAMESPACE}"; then
	uwskube create namespace "${TAPO_API_NAMESPACE}"
fi

if test "X${TAPO_CDN_NAMESPACE}" != "X${TAPO_NAMESPACE}"; then
	uwskube create namespace "${TAPO_CDN_NAMESPACE}"
fi

if test 'X' != "X${TAPO_WORKER_NAMESPACE}"; then
	uwskube create namespace "${TAPO_WORKER_NAMESPACE}"
fi

exit 0
