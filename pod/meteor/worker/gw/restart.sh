#!/bin/sh
set -eu
ns=worker
export METEOR_NAMESPACE=${ns}
export METEOR_TLS=uwsgd
export METEOR_HOST=${METEOR_WORKER_HOST}
exec ~/pod/meteor/gw/restart.sh "${ns}"
