#!/bin/sh
set -eu

cluster=${1:?'cluster?'}
kind=${2:?'kind?'}
action=${3:?'action?'}

shift 3

logs_dir=${HOME}/logs
logf=${logs_dir}/app-ctl.log

mkdir -vp "${logs_dir}"
echo "$(date -R): ${cluster} ${kind} ${action} ${*}" >>"${logf}"

cmd=./pod/${kind}/${action}.sh

cd /srv/uws/deploy
if ! test -x "${cmd}"; then
	echo "invalid action: ${action}" >&2
	exit 1
fi

exec ./docker/k8s/cli.sh "${cluster}" "${cmd}" "$@"
