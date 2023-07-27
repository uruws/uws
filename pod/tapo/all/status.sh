#!/bin/sh
set -eux
~/pod/tapo/worker/status.sh
~/pod/tapo/api/status.sh
~/pod/tapo/web/status.sh
exit 0
