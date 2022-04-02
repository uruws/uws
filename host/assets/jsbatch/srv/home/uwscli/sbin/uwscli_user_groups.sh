#!/bin/sh
set -eu

umask 0027

username=${1:?'user name?'}
shift

adduser "${username}" uwscli || true

for groupname in ${1}; do
	adduser "${username}" "${groupname}" || true
done

exit 0
