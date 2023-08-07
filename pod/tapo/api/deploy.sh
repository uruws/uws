#!/bin/sh
set -eu

appver=${1:?'app version?'}

METEOR_REPLICAS="${TAPO_API_REPLICAS}"
export METEOR_REPLICAS

METEOR_CPU_REQ="${TAPO_API_CPU_REQ}"
export METEOR_CPU_REQ

METEOR_CPU_MAX="${TAPO_API_CPU_MAX}"
export METEOR_CPU_MAX

exec ~/pod/tapo/deploy.sh "${TAPO_NAMESPACE}" api "${appver}"
