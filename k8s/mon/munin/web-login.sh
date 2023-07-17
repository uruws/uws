#!/bin/sh
set -eu
exec uwskube exec deployment/${UWS_CLUSTER}-munin -i -t -c munin-web -n mon -- bash -il
