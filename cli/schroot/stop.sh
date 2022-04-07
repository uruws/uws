#!/bin/sh
set -eu

profile=${1:?'profile?'}
service=${2:?'service?'}

if ! test -d /etc/schroot/uwscli-${profile}; then
	echo "invalid profile: ${profile}" >&2
	exit 1
fi

sess="uwscli-${profile}-${service}"
exec schroot -c ${sess} -e
