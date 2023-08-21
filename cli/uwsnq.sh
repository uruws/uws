#!/bin/sh
set -eu

NQDIR=/run/uwscli/nq
export NQDIR

user=${1:?'user?'}
shift

CMD=${1:?'cmd?'}
shift

if test "X${CMD}" != 'X/srv/uws/deploy/cli/app-build.sh'\
	&& test "X${CMD}" != 'X/srv/uws/deploy/cli/app-clean-build.sh'\
	&& test "X${CMD}" != 'X/srv/uws/deploy/cli/buildpack.sh'\
	&& test "X${CMD}" != 'X/srv/uws/deploy/cli/app-autobuild-deploy.sh'\
	&& test "X${CMD}" != 'X/srv/deploy/Buildpack/build.py'
then
	echo "uwsnq invalid command: ${CMD}" >&2
	exit 9
fi

logd=${HOME}/logs
logf=${logd}/uwsq.log
install -d -m 0750 "${logd}"

export SUDO_USER

if test "X${CMD}" = 'X/srv/deploy/Buildpack/build.py'; then
	/srv/uws/deploy/cli/botija.sh "[${user}] ${CMD} ${*}"
fi

echo "$(date -R) [${user}] ${CMD} ${*}" >>"${logf}"
exec nq -c -- "${CMD}" "$@"
