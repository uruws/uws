#!/bin/sh
set -eu
cluster=${1:?'cluster?'}
shift
export UWSEKSCMD='true'
exec ./docker/eks/admin.sh "${cluster}" --client "$@"
