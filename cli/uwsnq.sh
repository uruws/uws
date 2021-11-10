#!/bin/sh
set -eu
export NQDIR=/run/uwscli/nq
mkdir -p -m 0750 ${NQDIR}
user=${1:?'user?'}
shift
CMD=${1:?'cmd?'}
shift
if test "X${CMD}" != 'X/srv/uws/deploy/cli/app-build.sh'\
	&& test "X${CMD}" != 'X/srv/uws/deploy/cli/app-clean-build.sh'\
	&& test "X${CMD}" != 'X/srv/deploy/Buildpack/build.py';
then
	echo "${CMD}: invalid command" >&2
	exit 9
fi
logd=${HOME}/logs
logf=${logd}/uwsq.log
mkdir -p -m 0750 "${logd}"
echo "$(date -R) [${user}] ${CMD} ${*}" >>"${logf}"
exec nq -c -- "${CMD}" "$@"
