#!/bin/sh
set -eu

umask 0027

if test $# -eq 0; then
	exit 0
fi

for username in ${1}; do
	adduser "${username}" uwsops
done

exit 0
