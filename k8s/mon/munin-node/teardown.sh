#!/bin/sh
set -u
exec uwskube delete svc munin-node -n mon
