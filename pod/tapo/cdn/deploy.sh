#!/bin/sh
set -eu

appver=${1:?'app version?'}

METEOR_REPLICAS="${TAPO_CDN_REPLICAS}"
export METEOR_REPLICAS

METEOR_CPU="${TAPO_CPU}"
export METEOR_CPU

METEOR_MEMORY="${TAPO_MEMORY}"
export METEOR_MEMORY

exec ~/pod/tapo/deploy.sh tapo cdn "${appver}"
