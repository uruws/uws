#!/bin/sh
set -eu
exec ~/pod/lib/logs.py -n netdata -l 'app=netdata' "$@"
