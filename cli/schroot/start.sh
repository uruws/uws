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

schroot -c uwscli-${profile} -n ${sess} -b

trap cleanup INT EXIT

schroot_cmd="schroot -c ${sess} -d /root -u root -r"

${schroot_cmd} -- /srv/home/uwscli/sbin/${service}_init.sh

exit 0
