#!/bin/sh
set -eu

DOCKER_RUN_ARGS="--rm"
export DOCKER_RUN_ARGS

exec ./docker/asb/devel.sh "$@"
