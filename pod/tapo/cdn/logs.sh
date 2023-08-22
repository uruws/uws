#!/bin/sh
set -eu
exec ~/pod/tapo/logs.sh "${TAPO_CDN_NAMESPACE}" cdn "$@"
