#!/bin/sh
set -eu
ns=${TAPO_API_NAMESPACE}
exec ~/pod/tapo/ngx/setup.sh "${ns}"
