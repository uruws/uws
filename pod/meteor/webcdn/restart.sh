#!/bin/sh
set -eu
~/pod/meteor/webcdn/configure.sh
exec uwskube rollout restart deployment -n webcdn
