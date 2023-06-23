#!/bin/sh
set -eu

/root/bin/msmtprc-install.sh syslog root

start_cron() (
	sleep 3
	/etc/init.d/cron start
)

start_cron &

exec /usr/sbin/rsyslogd -n
