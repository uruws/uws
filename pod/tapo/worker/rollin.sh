#!/bin/sh
set -eu
exec ~/pod/tapo/rollin.sh "${TAPO_WORKER_NAMESPACE}" worker
