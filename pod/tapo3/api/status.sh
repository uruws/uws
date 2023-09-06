#!/bin/sh
set -eu
exec ~/pod/lib/tapo3/status.sh "${TAPO3_API_NAMESPACE}" api
