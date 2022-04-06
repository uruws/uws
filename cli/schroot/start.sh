#!/bin/sh
set -eu

profile=${1:?'profile?'}

if ! test -d /etc/schroot/uwscli-${profile}; then
	echo "invalid profile: ${profile}" >&2
	exit 1
fi

sess=$(schroot -c uwscli-${profile} -b)

cleanup() {
	schroot -c ${sess} -e
}

trap cleanup INT EXIT

schroot_sess="schroot -c ${sess} -r"

${schroot_sess} -d /root -u root -- /srv/home/uwscli/sbin/sshd_init.sh

exit 0
