#!/bin/sh
set -eux

/etc/init.d/munin start
/etc/init.d/munin-node start

/etc/init.d/cron start

rm -vf /var/log/munin/*.log \
	&& ln -vsf /dev/stderr /var/log/munin/munin-node.log \
	&& ln -vsf /dev/stderr /var/log/munin/munin-update.log

exec rsyslogd -n
