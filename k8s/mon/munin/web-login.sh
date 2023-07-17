#!/bin/sh
set -eu
exec uwskube exec deployment/munin -i -t -c munin-web -n mon -- bash -il
