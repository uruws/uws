#!/bin/sh
set -eux
~/pod/tapo/worker/restart.sh
~/pod/tapo/api/restart.sh
~/pod/tapo/web/restart.sh
exit 0
