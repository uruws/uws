#!/bin/sh
set -eu
ns=worker
export METEOR_NAMESPACE=${ns}
export METEOR_TLS=uwsgd
export METEOR_HOST=${METEOR_WORKER_HOST}
export NGINX_REPLICAS=${METEOR_WORKER_REPLICAS}
exec ~/pod/meteor/gw/deploy.sh "${ns}"