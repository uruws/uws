#!/bin/sh
set -eu

profile=${1:?'profile?'}

if ! test -d /etc/schroot/uwscli-${profile}; then
	echo "invalid profile: ${profile}" >&2
	exit 1
fi

sess="uwscli-${profile}"
schroot_sess="schroot -c ${sess} -d /root -u root -r"

cleanup() {
	schroot -c ${sess} -e || true
}

trap cleanup INT

schroot -c uwscli-${profile} -n ${sess} -b

set +e
${schroot_sess} -- /srv/home/uwscli/sbin/uwscli_init.sh "${profile}"
exit 0
