#!/bin/sh
set -eu
echo 'EXTRA_OPTS="-L 5"' >>/etc/default/cron
ln -svf /etc/monit/conf-available/cron /etc/monit/conf-enabled
/etc/init.d/cron start
exit 0
