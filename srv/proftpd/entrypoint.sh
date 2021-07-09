#!/bin/sh
set -eu
ln -svf /run/sftp.log /dev/stdout
exec /usr/sbin/proftpd -n -4 -S 0.0.0.0 -d 3
