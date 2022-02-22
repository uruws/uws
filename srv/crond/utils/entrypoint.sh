#!/bin/sh
set -eu

start_cron() (
	sleep 3
	/etc/init.d/cron start
)

start_cron &

exec /usr/sbin/rsyslogd -n
