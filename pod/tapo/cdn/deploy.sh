#!/bin/sh
set -eu

appver=${1:?'app version?'}

METEOR_REPLICAS="${TAPO_CDN_REPLICAS}"
export METEOR_REPLICAS

METEOR_REPLICAS_MAX="${TAPO_CDN_REPLICAS_MAX}"
export METEOR_REPLICAS_MAX

METEOR_CPU_REQ="${TAPO_CDN_CPU_REQ}"
export METEOR_CPU_REQ

METEOR_CPU_MAX="${TAPO_CDN_CPU_MAX}"
export METEOR_CPU_MAX

METEOR_HPA_ENABLE="${TAPO_CDN_HPA_ENABLE}"
export METEOR_HPA_ENABLE

METEOR_HPA_CPU="${TAPO_CDN_HPA_CPU}"
export METEOR_HPA_CPU

exec ~/pod/tapo/deploy.sh "${TAPO_CDN_NAMESPACE}" cdn "${appver}"
