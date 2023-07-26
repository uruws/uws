#!/bin/sh
set -eu
exec ~/pod/tapo/logs.sh "${TAPO_WORKER_NAMESPACE}" worker
