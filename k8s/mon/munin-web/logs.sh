#!/bin/sh
set -eu
exec uwskube logs pod/munin-web-0 -n mon $*
