#!/bin/sh
set -eu

pldir=/uws/lib/plugins
export PYTHONPATH=${pldir}

mod=$(basename ${0})
#~ echo "MOD: ${mod}"

action=${1:-'report'}

k8s_setup() (
	if test -d /uws/etc/cluster; then
		dst=/uws/etc/cluster.json
		echo '[' >${dst}
		for fn in /uws/etc/cluster/*.env; do
			# shellcheck disable=SC1090
			. ${fn}
			cat <<EOF >>${dst}
  {
    "name": "${UWS_CLUSTER}",
    "host": "${CLUSTER_HOST}"
  },
EOF
		done
		echo '  {}' >>${dst}
		echo ']' >>${dst}
		ls -lh ${dst}
	fi
)

pl_setup() {
	for fn in ${pldir}/cluster*.py; do
		p=$(basename ${fn} .py)
		install -v -C -m 0750 -g uws /uws/bin/mnpl.sh /etc/munin/plugins/${p}
	done
}

if test "X${mod}" = 'Xmnpl.sh'; then
	if test "X${action}" = 'Xsetup'; then
		k8s_setup
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
