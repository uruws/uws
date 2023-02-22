#!/bin/sh
set -eu
exec uwskube exec deploy/munin-node -i -t -n mon -- bash -il
