#!/bin/sh
set -eu
exec uwskube exec deployment/munin -i -t -c ${UWS_CLUSTER}-munin -n mon -- bash -il
