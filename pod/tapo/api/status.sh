#!/bin/sh
set -eu
exec ~/pod/tapo/status.sh "${TAPO_NAMESPACE}" api
