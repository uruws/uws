#!/bin/sh
set -eu
exec ~/pod/tapo/restart.sh "${TAPO_WORKER_NAMESPACE}" worker
