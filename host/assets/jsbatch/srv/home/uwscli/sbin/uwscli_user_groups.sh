#!/bin/sh
set -eu

umask 0027

username=${1:?'user name?'}
shift

adduser "${username}" uwscli || true

if test $# -ne 1; then
	echo 'uwscli_user_groups.sh: no groups' >&2
	exit 0
fi

for groupname in ${1}; do
	adduser "${username}" "${groupname}" || true
done

exit 0
