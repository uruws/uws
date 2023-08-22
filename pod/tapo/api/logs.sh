#!/bin/sh
set -eu
exec ~/pod/tapo/logs.sh "${TAPO_API_NAMESPACE}" api "$@"
