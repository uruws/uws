#!/bin/sh
set -u
exec uwskube delete svc munin-web -n mon --wait
