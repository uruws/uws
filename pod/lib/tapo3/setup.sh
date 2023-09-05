#!/bin/sh
set -eu

uwskube create namespace "${TAPO3_NAMESPACE}"

if test 'X' != "X${TAPO3_API_NAMESPACE}"; then
	uwskube create namespace "${TAPO3_API_NAMESPACE}"
fi

if test 'X' != "X${TAPO3_CDN_NAMESPACE}"; then
	uwskube create namespace "${TAPO3_CDN_NAMESPACE}"
fi

if test 'X' != "X${TAPO3_WORKER_NAMESPACE}"; then
	uwskube create namespace "${TAPO3_WORKER_NAMESPACE}"
fi

exit 0
