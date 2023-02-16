#!/bin/sh
set -eu

install -v -d -m 0775 -o munin -g www-data /var/lib/munin/cgi-tmp

#chown -v munin:adm /var/log/munin
#chmod -v 0755 /var/log/munin

mkdir -vp /var/opt/munin-alert
chmod -v 1777 /var/opt/munin-alert

mkdir -vp /var/opt/munin-alert/statuspage
chmod -v 1777 /var/opt/munin-alert/statuspage

# CA
if test -d /srv/etc/ca; then
	install -v -d -m 0750 -o root -g munin /etc/opt/uws/ca
	install -v -m 0640 -o root -g munin \
		/srv/etc/ca/08082dca-8d77-5c81-9a44-94642089b3b1.pem \
		/etc/opt/uws/ca/smtps.pem
	install -v -m 0640 -o root -g munin \
		/srv/etc/ca/08082dca-8d77-5c81-9a44-94642089b3b1.key \
		/etc/opt/uws/ca/smtps.key
fi

# /etc/cron.d
if test -d /srv/etc/cron.d; then
	cp -vrf /srv/etc/cron.d /etc
	chown -v root:root /etc/cron.d/uws-*
	chmod -v 0640 /etc/cron.d/uws-*
fi

# /etc/munin
if test -d /srv/etc/munin; then
	cp -vrf /srv/etc/munin /etc
fi
chown -v root:munin /etc/munin/munin.conf /etc/munin/munin-conf.d/*.conf || true
chmod -v 0640 /etc/munin/munin.conf /etc/munin/munin-conf.d/*.conf || true

# /etc/uws/conf
if test -d /etc/uws/conf; then
	install -v -o root -g munin \
		/etc/uws/conf/alerts_conf.json /etc/uws/munin/alerts_conf.json
fi

###/opt/munin/bin/k8s-setup.py

/etc/init.d/munin start
/etc/init.d/cron start

exec rsyslogd -n
