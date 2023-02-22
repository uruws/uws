#!/bin/sh
set -eu
exec uwskube exec deployment/munin-node -n mon -- munin-run "$@"
