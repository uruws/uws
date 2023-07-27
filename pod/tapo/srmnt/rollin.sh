#!/bin/sh
set -eux
export TAPO_ENV="${SRMNT_ENV}"
export TAPO_NAMESPACE="${SRMNT_NAMESPACE}"
~/pod/tapo/api/rollin.sh
~/pod/tapo/web/rollin.sh
exit 0
