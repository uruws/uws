#!/bin/sh
set -eu
exec uwskube exec pod/${UWS_CLUSTER}-munin-0 -i -t -c munin -n mon -- tail "${@}" /var/log/munin/munin-graph.log /var/log/munin/munin-html.log /var/log/munin/munin-limits.log /var/log/munin/munin-update.log
