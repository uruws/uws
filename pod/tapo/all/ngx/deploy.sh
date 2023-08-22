#!/bin/sh
set -eux
~/pod/tapo/cdn/ngx/deploy.sh
~/pod/tapo/api/ngx/deploy.sh
~/pod/tapo/web/ngx/deploy.sh
exit 0
