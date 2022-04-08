#!/bin/sh
set -eu

profile=${1:?'profile?'}

if ! test -d ./cli/schroot/${profile}; then
	echo "invalid profile: ${profile}" >&2
	exit 1
fi

sess=$(schroot -c uwscli-${profile} -b)
schroot_sess="schroot -c ${sess} -d /root -u root -r"

cleanup() {
	${schroot_sess} -- /etc/init.d/docker stop
	schroot -c ${sess} -e
}

trap cleanup INT EXIT

${schroot_sess} -- /etc/init.d/docker start
sleep 1
${schroot_sess} -- /bin/bash -i

exit 0
