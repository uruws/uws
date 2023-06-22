#!/bin/sh
set -eux

# munin dirs

if test -d /efs/munin-log; then
	install -v -d /efs/munin-log/data/munin-log
	rm -rf /var/log/munin
	ln -sv /efs/munin-log/data/munin-log /var/log/munin
else
	install -v -d -m 0755 -o munin -g adm /var/log/munin
	chown -R munin:adm /var/log/munin
fi

if test -d /efs/munin-db; then
	install -v -d /efs/munin-db/data/munin-db
	rm -rf /var/lib/munin
	ln -sv /efs/munin-db/data/munin-db /var/lib/munin
else
	install -v -d -m 0755 -o munin -g munin /var/lib/munin
	chown -R munin:munin /var/lib/munin
fi

if test -d /efs/munin-cache; then
	install -v -d /efs/munin-cache/data/munin-cache
	rm -rf /var/cache/munin/www
	ln -sv /efs/munin-cache/data/munin-cache /var/cache/munin/www
else
	install -v -d -m 0755 -o munin -g munin /var/cache/munin/www
	chown -R munin:munin /var/cache/munin/www
fi

# alerts dirs

install -v -d -m 1777 /var/opt/munin-alert
install -v -d -m 1777 /var/opt/munin-alert/amazon-ses

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

exec /usr/sbin/rsyslogd -n
