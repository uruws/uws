#!/bin/sh
set -u
ns=${TAPO_API_NAMESPACE}
exec ~/pod/tapo/ngx/teardown.sh "${ns}"
