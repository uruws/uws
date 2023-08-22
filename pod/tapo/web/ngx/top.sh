#!/bin/sh
set -eu
ns=${TAPO_NAMESPACE}
exec ~/pod/tapo/ngx/top.sh "${ns}"
