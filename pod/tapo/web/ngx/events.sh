#!/bin/sh
set -eu
ns=${TAPO_NAMESPACE}
exec ~/pod/tapo/ngx/events.sh "${ns}" "$@"
