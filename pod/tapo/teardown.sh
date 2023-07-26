#!/bin/sh
set -u
uwskube delete namespace "${TAPO_WORKER_NAMESPACE}"
uwskube delete namespace "${TAPO_NAMESPACE}"
exit 0
