#!/bin/sh
set -eu
exec ~/pod/tapo/status.sh "${TAPO_WORKER_NAMESPACE}" worker
