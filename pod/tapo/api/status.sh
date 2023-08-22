#!/bin/sh
set -eu
exec ~/pod/tapo/status.sh "${TAPO_API_NAMESPACE}" api
