#!/bin/sh
set -eu
replicas=${1:?'app replicas?'}
exec ~/pod/tapo/scale.sh "${TAPO_CDN_NAMESPACE}" cdn "${replicas}"
