#!/bin/sh
set -eu
exec uwskube exec svc/munin-node -i -t -n mon -- bash -il
