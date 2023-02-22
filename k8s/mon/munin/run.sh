#!/bin/sh
set -eu
exec uwskube exec pod/munin-0 -c munin -n mon -- munin-run "$@"
