#!/bin/sh
set -eux

export TAPO_ENV="${SRMNT_ENV}"
export TAPO_NAMESPACE="${SRMNT_NAMESPACE}"
export TAPO_WORKER_NAMESPACE="${SRMNT_WORKER_NAMESPACE}"

exec ~/pod/tapo/setup.sh
