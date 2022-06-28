#!/bin/sh
set -eu

mkdir -vp /var/lib/munin/cgi-tmp

chown -v munin:munin /var/lib/munin
chmod -v 0755 /var/lib/munin

chown -v munin:www-data /var/lib/munin/cgi-tmp
chmod -v 0775 /var/lib/munin/cgi-tmp

chown -v munin:adm /var/log/munin
chmod -v 0755 /var/log/munin

mkdir -vp /var/opt/munin-alert
chmod -v 1777 /var/opt/munin-alert

mkdir -vp /var/opt/munin-alert/statuspage
chmod -v 1777 /var/opt/munin-alert/statuspage

if test -d /srv/etc/ca; then
	install -v -d -m 0750 -o root -g munin /etc/opt/uws/ca
	install -v -m 0640 -o root -g munin \
		/srv/etc/ca/08082dca-8d77-5c81-9a44-94642089b3b1.pem \
		/etc/opt/uws/ca/smtps.pem
	install -v -m 0640 -o root -g munin \
		/srv/etc/ca/08082dca-8d77-5c81-9a44-94642089b3b1.key \
		/etc/opt/uws/ca/smtps.key
fi

if test -d /srv/etc/munin; then
	cp -vrf /srv/etc/munin /etc
fi

chown -v root:munin /etc/munin/munin.conf /etc/munin/munin-conf.d/*.conf || true
chmod -v 0640 /etc/munin/munin.conf /etc/munin/munin-conf.d/*.conf || true

###/opt/munin/bin/k8s-setup.py

/etc/init.d/munin start
/etc/init.d/cron start

exec rsyslogd -n
