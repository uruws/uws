#!/bin/sh
set -eux
/etc/init.d/munin start
/etc/init.d/munin-node start
/etc/init.d/cron start
exec rsyslogd -n
