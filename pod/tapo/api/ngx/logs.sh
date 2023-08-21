#!/bin/sh
set -eu
ns=${TAPO_API_NAMESPACE}
exec ~/pod/tapo/ngx/logs.sh "${ns}" "$@"
