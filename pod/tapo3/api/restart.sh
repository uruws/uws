#!/bin/sh
set -eu
exec ~/pod/lib/tapo3/restart.sh "${TAPO3_API_NAMESPACE}" api
