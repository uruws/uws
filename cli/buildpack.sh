#!/bin/sh
set -eu

user=${1:?'user?'}
cluster=${2:?'cluster?'}
kind=${3:?'kind?'}
action=${4:?'action?'}

shift 4

logs_dir=${HOME}/logs
logf=${logs_dir}/app-ctl.log

mkdir -vp "${logs_dir}"
echo "$(date -R) [${user}] ${cluster} ${kind} ${action} ${*}" >>"${logf}"

cmd=./pod/${kind}/${action}.sh

cd /srv/uws/deploy
if ! test -x "${cmd}"; then
	echo "invalid action: ${action}" >&2
	exit 1
fi



exec /srv/deploy/Buildpack/build.py "$@"
