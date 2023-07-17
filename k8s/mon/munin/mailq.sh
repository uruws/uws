#!/bin/sh
set -eu
q=${1:-""}
exec uwskube exec deployment/munin -c ${UWS_CLUSTER}-munin -n mon -- \
	find "/var/opt/munin-alert/${q}" -maxdepth 1 -type f -name '*.eml'
