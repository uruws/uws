#!/bin/sh
set -eu

appver=${1:?'app version?'}

~/pod/tapo/cdn/deploy.sh "${appver}"
~/pod/tapo/cdn/wait.sh

METEOR_REPLICAS="${TAPO_REPLICAS}"
export METEOR_REPLICAS

METEOR_CPU="${TAPO_CPU}"
export METEOR_CPU

METEOR_MEMORY="${TAPO_MEMORY}"
export METEOR_MEMORY

exec ~/pod/tapo/deploy.sh "${TAPO_NAMESPACE}" web "${appver}"
