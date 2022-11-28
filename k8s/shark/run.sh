#!/bin/sh
set -eu
cluster=${1:?'cluster?'}
shift
./eks/cmd.sh "${cluster}" ./k8s/shark/start.sh "$@"
exit 0
