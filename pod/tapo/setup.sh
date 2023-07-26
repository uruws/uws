#!/bin/sh
set -eu
uwskube create namespace "${TAPO_NAMESPACE}"
uwskube create namespace "${TAPO_WORKER_NAMESPACE}"
exit 0
