#!/bin/sh
set -eu
exec ~/pod/lib/tapo3/ngx/logs.sh "${TAPO3_API_NAMESPACE}" api "$@"
