#!/bin/sh
set -eu

umask 0027

for username in $*; do
	adduser "${username}" uwsops
done

exit 0
