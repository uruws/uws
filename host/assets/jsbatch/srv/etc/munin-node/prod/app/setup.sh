#!/bin/sh
set -eu

pl_ena=/root/bin/plugin-enable.sh
${pl_ena} http_loadtime http_loadtime

rm -vf /etc/munin/plugins/uwsbot_stats
ln -svf /uws/bin/uwsbot-stats /etc/munin/plugins/uwsbot_stats

exit 0
