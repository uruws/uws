#!/bin/sh
set -eu

pldir=/uws/lib/plugins
export PYTHONPATH=${pldir}

mod=$(basename ${0})
#~ echo "MOD: ${mod}"

action=${1:-'report'}

pl_setup() {
	for fn in ${pldir}/*.py; do
		p=$(basename ${fn} .py)
		if test "X${p}" != 'Xmnpl'; then
			ln -sv ${fn} /etc/munin/plugins/${p}
		fi
	done
}

if test "X${mod}" = 'Xmnpl.sh'; then
	if test "X${action}" = 'Xsetup'; then
		pl_setup
		exit 0
	fi
	exit 9
fi

if ! test -f ${pldir}/${mod}.py; then
	echo "${mod}: invalid mnpl command" >&2
	exit 1
fi

exec /usr/bin/python3 -m ${mod} "$@"
