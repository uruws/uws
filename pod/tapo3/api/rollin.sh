#!/bin/sh
set -eu
exec ~/pod/lib/tapo3/rollin.sh "${TAPO3_API_NAMESPACE}" api
