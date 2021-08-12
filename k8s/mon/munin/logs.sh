#!/bin/sh
set -eu
exec uwskube logs pod/munin-0 -n mon $*
