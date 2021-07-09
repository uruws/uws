#!/bin/sh
set -eu
exec /usr/sbin/proftpd -n -4 -S 0.0.0.0 -d 3
