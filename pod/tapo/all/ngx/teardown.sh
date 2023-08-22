#!/bin/sh
set -eux
~/pod/tapo/cdn/ngx/teardown.sh
~/pod/tapo/api/ngx/teardown.sh
~/pod/tapo/web/ngx/teardown.sh
exit 0
