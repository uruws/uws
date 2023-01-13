#!/bin/sh
set -eu
cluster=${1:?'cluster?'}
exec ./docker/eks/admin.sh "${cluster}"
