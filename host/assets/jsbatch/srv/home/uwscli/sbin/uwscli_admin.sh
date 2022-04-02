#!/bin/sh
set -eu

umask 0027

addgroup uwsadm || true

for username in "$@"; do
	adduser "${username}" uwsadm
done

exit 0
