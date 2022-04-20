#!/bin/sh
set -eu

umask 0027

if test $# -eq 0; then
	exit 0
fi


# shellcheck disable=SC2048
for username in $*; do
	adduser "${username}" uwsops
done

exit 0
