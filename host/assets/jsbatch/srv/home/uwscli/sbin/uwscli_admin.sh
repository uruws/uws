#!/bin/sh
set -eu

umask 0027

groupname=${1:?'group name?'}
shift

addgroup "${groupname}" || true

for username in $*; do
	adduser "${username}" "${groupname}"
done

exit 0
