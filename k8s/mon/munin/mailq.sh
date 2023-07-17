#!/bin/sh
set -eu
q=${1:-""}
exec uwskube exec deployment/${UWS_CLUSTER}-munin -c munin -n mon -- \
	find "/var/opt/munin-alert/${q}" -maxdepth 1 -type f -name '*.eml'
