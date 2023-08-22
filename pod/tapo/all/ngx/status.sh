#!/bin/sh
set -eux
~/pod/tapo/cdn/ngx/status.sh
~/pod/tapo/api/ngx/status.sh
~/pod/tapo/web/ngx/status.sh
exit 0
