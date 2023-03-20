#!/bin/sh
set -eu
cluster=${1:?'cluster?'}
shift
exec ./eks/cmd.sh "${cluster}" ./k8s/mon/kubeshark/start.sh "${cluster}" "$@"
