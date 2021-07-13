#!/bin/sh
set -eu
exec /usr/sbin/proftpd -c /usr/local/etc/proftpd/proftpd.conf -n -4 -S 0.0.0.0 -d 2
