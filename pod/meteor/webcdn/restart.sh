#!/bin/sh
set -eu
~/pod/meteor/web/cdn/meteor-configure.sh
exec uwskube rollout restart deployment -n webcdn
