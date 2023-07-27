#!/bin/sh
set -eux
export TAPO_ENV="${SRMNT_ENV}"
export TAPO_NAMESPACE="${SRMNT_NAMESPACE}"
~/pod/tapo/api/restart.sh
~/pod/tapo/web/restart.sh
exit 0
