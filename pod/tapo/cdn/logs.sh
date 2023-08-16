#!/bin/sh
set -eu
exec ~/pod/tapo/logs.sh "${TAPO_NAMESPACE}" cdn "$@"
