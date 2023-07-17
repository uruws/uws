#!/bin/sh
set -eu
exec uwskube exec pod/${UWS_CLUSTER}-munin-0 -i -t -c munin -n mon -- bash -il
