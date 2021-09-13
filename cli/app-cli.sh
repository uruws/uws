#!/bin/sh
set -eu

cluster=${1:?'cluster?'}
kind=${2:?'kind?'}
action=${3:?'action?'}

shift 3

cmd=./pod/${kind}/${action}.sh

cd /srv/uws/deploy
if ! test -x "${cmd}"; then
	echo "invalid action: ${action}" >&2
	exit 1
fi

export DOCKER_ARGS='-it'
exec ./docker/k8s/cli.sh "${cluster}" "${cmd}" "$@"
