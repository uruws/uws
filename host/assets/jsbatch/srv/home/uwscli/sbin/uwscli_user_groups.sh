#!/bin/sh
set -eux

umask 0027

username=${1:?'user name?'}
shift

adduser "${username}" uwscli || true

if test $# -eq 0; then
	echo 'uwscli_user_groups.sh: no groups' >&2
	exit 0
fi

for groupname in "$@"; do
	adduser "${username}" "${groupname}"
done

exit 0
