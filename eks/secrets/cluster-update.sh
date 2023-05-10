#!/bin/sh
set -eu

ef=${1:?'env file?'}

. "${ef}"

echo "*** secrets update: ${UWS_CLUSTER}"
exec ./eks/secrets/cluster.py --profile "${AWS_PROFILE}" "${UWS_CLUSTER}"
