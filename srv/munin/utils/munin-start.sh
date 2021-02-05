#!/bin/sh
set -eux

mkdir -vp /var/lib/munin/cgi-tmp
chown -v munin:munin /var/lib/munin
chmod -v 0755 /var/lib/munin

chown -v munin:www-data /var/lib/munin/cgi-tmp
chmod -v 0775 /var/lib/munin/cgi-tmp

chown -v munin:munin /var/cache/munin/www
chmod -v 0755 /var/cache/munin/www

chown -v munin:adm /var/log/munin
chmod -v 0755 /var/log/munin

chown -v root:root /var/log/munin/munin-node.log
chown -v munin:munin /var/log/munin/munin-update.log
chmod -v 0644 /var/log/munin/*.log

/etc/init.d/munin start
/etc/init.d/munin-node start

/etc/init.d/cron start

exec rsyslogd -n
