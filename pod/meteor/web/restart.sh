#!/bin/sh
set -eu
echo 'webcdn'
~/pod/meteor/webcdn/restart.sh
~/pod/meteor/webcdn/wait.sh
echo 'web'
~/pod/meteor/web/configure.sh
exec uwskube rollout restart deployment -n web
