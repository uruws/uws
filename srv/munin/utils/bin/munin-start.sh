#!/bin/sh
set -eux

# munin dirs

install -v -d -m 0755 -o munin -g adm /var/log/munin
chown -R munin:adm /var/log/munin

install -v -d -m 0755 -o munin -g munin /var/lib/munin
chown -R munin:munin /var/lib/munin

install -v -d -m 0755 -o munin -g munin /var/cache/munin/www
chown -R munin:munin /var/cache/munin/www

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

# mailx

if test -d /srv/mailx/setup; then
	/root/bin/msmtprc-setup.sh
elif test -d /srv/mailx/etc; then
	/root/bin/msmtprc-install.sh syslog root
	/root/bin/msmtprc-install.sh syslog munin
	/root/bin/msmtprc-install.sh syslog www-data
	ln -svf /etc/opt/mailx/munin/msmtprc /var/lib/munin/.msmtprc
fi

###/opt/munin/bin/k8s-setup.py

/etc/init.d/munin start
/etc/init.d/cron start

exec /usr/sbin/rsyslogd -n
