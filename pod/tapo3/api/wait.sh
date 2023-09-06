#!/bin/sh
set -eu
exec ~/pod/lib/tapo3/wait.sh "${TAPO3_API_NAMESPACE}" api
