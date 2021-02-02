#!/bin/sh
set -eu
/etc/init.d/munin start
/etc/init.d/munin-node start
exec cron -f -L3
