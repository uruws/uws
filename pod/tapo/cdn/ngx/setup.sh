#!/bin/sh
set -eu
ns=${TAPO_CDN_NAMESPACE}
exec ~/pod/tapo/ngx/setup.sh "${ns}"
