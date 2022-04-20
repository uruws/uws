#!/bin/sh
set -eu

umask 0027

for groupname in "$@"; do
	addgroup "${groupname}" || true
done

exit 0
