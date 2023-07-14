#!/bin/sh
set -eu

appver=${1:?'app version?'}

METEOR_REPLICAS="${TAPO_WORKER_REPLICAS}"
export METEOR_REPLICAS

METEOR_CPU="${TAPO_WORKER_CPU}"
export METEOR_CPU

METEOR_MEMORY="${TAPO_WORKER_MEMORY}"
export METEOR_MEMORY

exec ~/pod/tapo/deploy.sh tpwrk worker "${appver}"
