#!/bin/sh
set -eu
cluster=${1:?'cluster?'}
kind=${2:?'web or worker?'}
action=${3:?'action?'}
if test "${action}" != 'restart' && test "${action}" != 'rollin'; then
	echo "invalid meteor action: ${action}" >&2
	exit 1
fi
cd /srv/uws/deploy
exec ./docker/k8s/cli.sh ${cluster} ./pod/meteor/${kind}/${action}.sh
