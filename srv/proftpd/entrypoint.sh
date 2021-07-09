#!/bin/sh
set -eu
#ln -svf /dev/stdout /run/sftp.log
#ls -lh /run
exec /usr/sbin/proftpd -n -4 -S 0.0.0.0 -d 3
