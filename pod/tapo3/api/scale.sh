#!/bin/sh
set -eu
replicas=${1:?'app replicas?'}
exec ~/pod/lib/tapo3/scale.sh "${TAPO3_API_NAMESPACE}" api "${replicas}"
