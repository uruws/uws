#!/bin/sh
set -eu

umask 0027

addgroup uwsadm || true

for username in ${1}; do
	adduser "${username}" uwsadm
done

exit 0
