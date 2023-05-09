#!/bin/sh
set -eu
exec ~/pod/lib/logs.py -n mon -c munin munin-0 "$@"
