#!/bin/sh
set -eux
~/pod/tapo/cdn/ngx/restart.sh
~/pod/tapo/api/ngx/restart.sh
~/pod/tapo/web/ngx/restart.sh
exit 0
