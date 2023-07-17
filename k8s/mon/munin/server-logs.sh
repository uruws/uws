#!/bin/sh
set -eu
exec uwskube exec deployment/${UWS_CLUSTER}-munin -i -t -c munin -n mon -- tail "${@}" /var/log/munin/munin-graph.log /var/log/munin/munin-html.log /var/log/munin/munin-limits.log /var/log/munin/munin-update.log
