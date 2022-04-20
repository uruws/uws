#!/bin/sh
set -eux

umask 0027

if test $# -eq 0; then
	exit 0
fi

for username in "$@"; do
	adduser "${username}" uwsadm
done

exit 0
