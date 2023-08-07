#!/bin/sh
set -eu

appver=${1:?'app version?'}

METEOR_REPLICAS="${TAPO_CDN_REPLICAS}"
export METEOR_REPLICAS

METEOR_CPU="${TAPO_CDN_CPU}"
export METEOR_CPU

METEOR_MEMORY="${TAPO_CDN_MEMORY}"
export METEOR_MEMORY

exec ~/pod/tapo/deploy.sh "${TAPO_NAMESPACE}" cdn "${appver}"
