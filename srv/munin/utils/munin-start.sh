#!/bin/sh
set -eu

mkdir -vp /var/lib/munin/cgi-tmp

chown -v munin:munin /var/lib/munin
chmod -v 0755 /var/lib/munin

chown -v munin:www-data /var/lib/munin/cgi-tmp
chmod -v 0775 /var/lib/munin/cgi-tmp

chown -v munin:adm /var/log/munin
chmod -v 0755 /var/log/munin

rm -vf /var/log/munin/*.log

if test -d /srv/etc/munin; then
	cp -vrf /srv/etc/munin /etc/munin
fi

chown -v root:munin /etc/munin/munin.conf /etc/munin/munin-conf.d/*.conf
chmod -v 0640 /etc/munin/munin.conf /etc/munin/munin-conf.d/*.conf

/etc/init.d/munin start
/etc/init.d/cron start

exec rsyslogd -n
