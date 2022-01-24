#!/bin/sh
set -eu

pldir=/uws/lib/plugins
export PYTHONPATH=${pldir}

mod=$(basename ${0})
#~ echo "MOD: ${mod}"

if ! test -f ${pldir}/${mod}.py; then
	echo "${mod}: invalid mnpl command" >&2
	exit 1
fi

exec /usr/bin/python3 -m ${mod} "$@"
