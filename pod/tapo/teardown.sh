#!/bin/sh
set -u
if test 'X' != "X${TAPO_WORKER_NAMESPACE}"; then
	uwskube delete namespace "${TAPO_WORKER_NAMESPACE}"
fi
uwskube delete namespace "${TAPO_NAMESPACE}"
exit 0
