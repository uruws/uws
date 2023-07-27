#!/bin/sh
set -eux
~/pod/tapo/worker/rollin.sh
~/pod/tapo/api/rollin.sh
~/pod/tapo/web/rollin.sh
exit 0
