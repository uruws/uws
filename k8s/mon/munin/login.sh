#!/bin/sh
set -eu
exec uwskube exec pod/munin-0 -i -t -c ${UWS_CLUSTER}-munin -n mon -- bash -il
