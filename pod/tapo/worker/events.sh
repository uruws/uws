#!/bin/sh
set -eu
exec ~/pod/tapo/events.sh "${TAPO_WORKER_NAMESPACE}" "$@"
