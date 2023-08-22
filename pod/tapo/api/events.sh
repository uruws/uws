#!/bin/sh
set -eu
exec ~/pod/tapo/events.sh "${TAPO_API_NAMESPACE}" "$@"
