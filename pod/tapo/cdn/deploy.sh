#!/bin/sh
set -eu

appver=${1:?'app version?'}

METEOR_REPLICAS="${TAPO_CDN_REPLICAS}"
export METEOR_REPLICAS

METEOR_CPU_REQ="${TAPO_CDN_CPU_REQ}"
export METEOR_CPU_REQ

METEOR_CPU_MAX="${TAPO_CDN_CPU_MAX}"
export METEOR_CPU_MAX

METEOR_HPA_ENABLE="${TAPO_CDN_HPA_ENABLE}"
export METEOR_HPA_ENABLE

exec ~/pod/tapo/deploy.sh "${TAPO_NAMESPACE}" cdn "${appver}"
