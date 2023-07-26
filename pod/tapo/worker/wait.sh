#!/bin/sh
set -eu
exec ~/pod/tapo/wait.sh "${TAPO_WORKER_NAMESPACE}" worker
