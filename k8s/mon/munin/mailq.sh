#!/bin/sh
set -eu
q=${1:-""}
exec find "/var/opt/munin-alert/${q}" -maxdepth 1 -type f -name '*.eml'
