#!/bin/sh
set -eu

appver=${1:?'app version?'}

METEOR_REPLICAS="${TAPO3_API_REPLICAS}"
export METEOR_REPLICAS

METEOR_REPLICAS_MAX="${TAPO3_API_REPLICAS_MAX}"
export METEOR_REPLICAS_MAX

METEOR_CPU_REQ="${TAPO3_API_CPU_REQ}"
export METEOR_CPU_REQ

METEOR_CPU_MAX="${TAPO3_API_CPU_MAX}"
export METEOR_CPU_MAX

METEOR_HPA_ENABLE="${TAPO3_API_HPA_ENABLE}"
export METEOR_HPA_ENABLE

METEOR_HPA_CPU="${TAPO3_API_HPA_CPU}"
export METEOR_HPA_CPU

exec ~/pod/lib/tapo3/deploy.sh "${TAPO3_API_NAMESPACE}" api "${appver}"
