#!/bin/sh
set -eux
export TAPO_ENV="${SRMNT_ENV}"
export TAPO_NAMESPACE="${SRMNT_NAMESPACE}"
exec ~/pod/tapo/events.sh "${TAPO_NAMESPACE}" "$@"
