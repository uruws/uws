#!/bin/sh
set -eu

umask 0027

for groupname in ${1}; do
	addgroup "${groupname}" || true
done

exit 0
