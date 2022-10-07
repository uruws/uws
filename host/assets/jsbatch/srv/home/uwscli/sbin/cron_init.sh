#!/bin/sh
set -eu
ln -svf /etc/monit/conf-available/cron /etc/monit/conf-enabled
/etc/init.d/cron start
exit 0
