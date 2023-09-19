#!/bin/sh
set -eu

appver=${1:?'app version?'}

if test 'X' = "X${TAPO_WORKER_NAMESPACE}"; then
	exit 0
fi

METEOR_REPLICAS="${TAPO_WORKER_REPLICAS}"
export METEOR_REPLICAS

METEOR_REPLICAS_MAX="${TAPO_WORKER_REPLICAS_MAX}"
export METEOR_REPLICAS_MAX

METEOR_MEMORY="${TAPO_WORKER_MEMORY}"
export METEOR_MEMORY

METEOR_CPU_REQ="${TAPO_WORKER_CPU_REQ}"
export METEOR_CPU_REQ

METEOR_CPU_MAX="${TAPO_WORKER_CPU_MAX}"
export METEOR_CPU_MAX

METEOR_HPA_ENABLE="${TAPO_WORKER_HPA_ENABLE}"
export METEOR_HPA_ENABLE

METEOR_HPA_CPU="${TAPO_WORKER_HPA_CPU}"
export METEOR_HPA_CPU

exec ~/pod/tapo/deploy.sh "${TAPO_WORKER_NAMESPACE}" worker "${appver}"
