#!/bin/sh
set -eu

ef=${1:?'env file?'}

# shellcheck disable=SC1090
. "${ef}"

exec ./eks/secrets/cluster.py --profile "${AWS_PROFILE}" "${UWS_CLUSTER}"
