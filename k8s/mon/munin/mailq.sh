#!/bin/sh
set -eu
q=${1:-""}
exec uwskube exec pod/munin-0 -c munin -n mon -- \
	find "/var/opt/munin-alert/${q}" -maxdepth 1 -type f -name '*.eml'
