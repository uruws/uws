#!/bin/sh
set -eu
exec ~/pod/tapo/restart.sh "${TAPO_API_NAMESPACE}" api
