#!/bin/sh
set -eux
export TAPO_ENV="${SRMNT_ENV}"
export TAPO_NAMESPACE="${SRMNT_NAMESPACE}"
~/pod/tapo/api/status.sh
~/pod/tapo/web/status.sh
exit 0
