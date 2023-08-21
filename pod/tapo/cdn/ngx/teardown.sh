#!/bin/sh
set -u
ns=${TAPO_CDN_NAMESPACE}
exec ~/pod/tapo/ngx/teardown.sh "${ns}"
