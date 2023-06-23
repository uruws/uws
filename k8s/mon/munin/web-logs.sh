#!/bin/sh
set -eu
exec ~/pod/lib/logs.py -n mon -c munin-web pod/munin-0 "$@"
