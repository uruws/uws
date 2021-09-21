#!/bin/sh
set -eu
export NQDIR=/run/uwscli/nq
mkdir -p -m 0750 ${NQDIR}
CMD=${1:?'cmd?'}
shift
if test "X${CMD}" != 'X/srv/uws/deploy/cli/app-build.sh'\
	&& test "X${CMD}" != 'X/srv/deploy/Buildpack/build.py'; then
	echo "${CMD}: invalid command" >&2
	exit 9
fi
exec nq -c -- "${CMD}" "$@"
