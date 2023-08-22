#!/bin/sh
set -eu
ns=${TAPO_NAMESPACE}
exec ~/pod/tapo/ngx/status.sh "${ns}"
