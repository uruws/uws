#!/bin/sh
set -eu
export TAPO_WORKER_NAMESPACE="${SRMNT_WORKER_NAMESPACE}"
exec ~/pod/tapo/worker/status.sh
