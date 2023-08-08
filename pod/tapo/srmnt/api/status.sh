#!/bin/sh
set -eu
export TAPO_NAMESPACE="${SRMNT_NAMESPACE}"
exec ~/pod/tapo/api/status.sh
