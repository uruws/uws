#!/bin/sh
set -eu
exec uwskube scale sts munin --replicas=0 -n mon
