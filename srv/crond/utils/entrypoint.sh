#!/bin/sh
set -eu

if test -d /srv/etc/ca; then
	group='root'
	install -v -d -m 0750 -o root -g ${group} /etc/opt/uws/ca
	install -v -m 0640 -o root -g ${group} \
		/srv/etc/ca/08082dca-8d77-5c81-9a44-94642089b3b1.pem \
		/etc/opt/uws/ca/smtps.pem
	install -v -m 0640 -o root -g ${group} \
		/srv/etc/ca/08082dca-8d77-5c81-9a44-94642089b3b1.key \
		/etc/opt/uws/ca/smtps.key
fi

/etc/init.d/cron start

exec /usr/sbin/rsyslogd -n
