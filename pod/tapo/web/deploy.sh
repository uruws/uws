#!/bin/sh
set -eu

appver=${1:?'app version?'}

~/pod/tapo/cdn/deploy.sh "${appver}"
~/pod/tapo/cdn/wait.sh

METEOR_REPLICAS="${TAPO_REPLICAS}"
export METEOR_REPLICAS

METEOR_CPU_REQ="${TAPO_CPU_REQ}"
export METEOR_CPU_REQ

METEOR_CPU_MAX="${TAPO_CPU_MAX}"
export METEOR_CPU_MAX

exec ~/pod/tapo/deploy.sh "${TAPO_NAMESPACE}" web "${appver}"
