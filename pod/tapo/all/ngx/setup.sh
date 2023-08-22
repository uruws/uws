#!/bin/sh
set -eux
~/pod/tapo/cdn/ngx/setup.sh
~/pod/tapo/api/ngx/setup.sh
~/pod/tapo/web/ngx/setup.sh
exit 0
