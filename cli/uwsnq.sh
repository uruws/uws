#!/bin/sh
set -eu
export NQDIR=/run/uwscli/nq
user=${1:?'user?'}
shift
CMD=${1:?'cmd?'}
shift
if test "X${CMD}" != 'X/srv/uws/deploy/cli/app-build.sh'\
	&& test "X${CMD}" != 'X/srv/uws/deploy/cli/app-clean-build.sh'\
	&& test "X${CMD}" != 'X/srv/uws/deploy/cli/buildpack.sh'
then
	echo "${CMD}: invalid command" >&2
	exit 9
fi
logd=${HOME}/logs
logf=${logd}/uwsq.log
install -d -m 0750 "${logd}"
echo "$(date -R) [${user}] ${CMD} ${*}" >>"${logf}"
exec nq -c -- "${CMD}" "$@"
