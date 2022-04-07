#!/bin/sh
set -eu

profile=${1:?'profile?'}
service=${2:?'service?'}

if ! test -d /etc/schroot/uwscli-${profile}; then
	echo "invalid profile: ${profile}" >&2
	exit 1
fi

sess="uwscli-${profile}-${service}"

cleanup() {
	schroot -c ${sess} -e
}

trap cleanup INT EXIT

schroot -c uwscli-${profile} -n ${sess} -b

schroot_sess="schroot -c ${sess} -r"

${schroot_sess} -d /root -u root -- /srv/home/uwscli/sbin/${service}_init.sh

exit 0
