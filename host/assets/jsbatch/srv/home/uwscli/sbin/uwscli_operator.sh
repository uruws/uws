#!/bin/sh
set -eu

umask 0027

for username in ${1}; do
	adduser "${username}" uwsops
done

exit 0
