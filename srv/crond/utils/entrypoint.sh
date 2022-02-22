#!/bin/sh
set -eu

/etc/init.d/cron start

exec /usr/sbin/rsyslogd -n
