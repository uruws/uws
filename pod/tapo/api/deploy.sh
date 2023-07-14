#!/bin/sh
set -eu

appver=${1:?'app version?'}

METEOR_REPLICAS="${TAPO_API_REPLICAS}"
export METEOR_REPLICAS

METEOR_CPU="${TAPO_API_CPU}"
export METEOR_CPU

METEOR_MEMORY="${TAPO_API_MEMORY}"
export METEOR_MEMORY

exec ~/pod/tapo/deploy.sh tapo api "${appver}"
