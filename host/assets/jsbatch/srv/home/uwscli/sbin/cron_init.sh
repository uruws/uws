#!/bin/sh
set -eu

echo 'EXTRA_OPTS="-L 5"' >>/etc/default/cron
ln -svf /etc/monit/conf-available/cron /etc/monit/conf-enabled
/etc/init.d/cron start

if test -s /usr/local/etc/crontab/uws.in; then
	crontab -u uws /usr/local/etc/crontab/uws.in
fi
if test -s /usr/local/etc/crontab/uwscli.in; then
	crontab -u uwscli /usr/local/etc/crontab/uwscli.in
fi

exit 0
