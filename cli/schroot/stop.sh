#!/bin/sh
set -eu

profile=${1:?'profile?'}

if ! test -d /etc/schroot/uwscli-${profile}; then
	echo "invalid profile: ${profile}" >&2
	exit 1
fi

sess="uwscli-${profile}"
schroot_sess="schroot -c ${sess} -d /root -u root -r"

${schroot_sess} -- /etc/init.d/docker stop || true
sleep 1

exec schroot -c ${sess} -e
