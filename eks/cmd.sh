#!/bin/sh
set -eu
cluster=${1:?'cluster?'}
shift
exec ./docker/eks/admin.sh ${cluster} --client "$@"
