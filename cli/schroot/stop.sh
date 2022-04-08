#!/bin/sh
set -eu

profile=${1:?'profile?'}

if ! test -d /etc/schroot/uwscli-${profile}; then
	echo "invalid profile: ${profile}" >&2
	exit 1
fi

sess="uwscli-${profile}"
exec schroot -c ${sess} -e
