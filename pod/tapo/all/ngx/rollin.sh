#!/bin/sh
set -eux
~/pod/tapo/cdn/ngx/rollin.sh
~/pod/tapo/api/ngx/rollin.sh
~/pod/tapo/web/ngx/rollin.sh
exit 0
