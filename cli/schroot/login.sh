#!/bin/sh
set -eu

profile=${1:?'profile?'}

if ! test -d ./cli/schroot/${profile}; then
	echo "invalid profile: ${profile}" >&2
	exit 1
fi

sess="uwscli-${profile}"
schroot_sess="schroot -c ${sess} -d /root -u root -r"

exec ${schroot_sess} -- /bin/bash -i
