#!/bin/sh
set -eu
exec ~/pod/tapo/events.sh "${TAPO_CDN_NAMESPACE}" "$@"
