#!/bin/sh
set -eu
exec ~/pod/lib/tapo3/events.sh "${TAPO3_API_NAMESPACE}" "$@"
