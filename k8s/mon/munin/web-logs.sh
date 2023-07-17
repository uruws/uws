#!/bin/sh
set -eu
exec ~/pod/lib/logs.py -n mon -c munin-web pod/${UWS_CLUSTER}-munin-0 "$@"
