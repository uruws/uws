#!/bin/sh
set -eu

if test -d /srv/mailx/setup/ca.client; then
	/root/bin/msmtprc-setup.sh
else
	/root/bin/msmtprc-install.sh syslog root
fi

start_cron() (
	sleep 3
	/etc/init.d/cron start
)

start_cron &

exec /usr/sbin/rsyslogd -n
