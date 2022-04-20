#!/bin/sh
set -eu

umask 0027

if test $# -eq 0; then
	echo 'uwscli_app.sh: no groups' >&2
	exit 0
fi

# shellcheck disable=SC2048
for groupname in $*; do
	addgroup "${groupname}" || true
done

exit 0
