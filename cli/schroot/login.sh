#!/bin/sh
set -eu

profile=${1:?'profile?'}

if ! test -d ./cli/schroot/${profile}; then
	echo "invalid profile: ${profile}" >&2
	exit 1
fi

sess=$(schroot -c uwscli-${profile} -b)

cleanup() {
	schroot -c ${sess} -e
}

trap cleanup INT EXIT

schroot_sess="schroot -c ${sess} -r"

${schroot_sess} -d /root -u root -- /bin/bash -i

exit 0
