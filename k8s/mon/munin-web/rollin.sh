#!/bin/sh
set -eu
exec uwskube scale sts munin-web --replicas=0 -n mon
