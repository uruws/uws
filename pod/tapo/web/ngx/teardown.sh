#!/bin/sh
set -u
ns=${TAPO_NAMESPACE}
exec ~/pod/tapo/ngx/teardown.sh "${ns}"