#!/bin/sh
set -eu
exec uwskube exec pod/munin-0 -i -t -c munin-web -n mon -- bash -il