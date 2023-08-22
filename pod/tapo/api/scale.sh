#!/bin/sh
set -eu
replicas=${1:?'app replicas?'}
exec ~/pod/tapo/scale.sh "${TAPO_API_NAMESPACE}" api "${replicas}"
