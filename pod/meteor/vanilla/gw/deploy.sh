#!/bin/sh
set -eu
ns=meteor-vanilla
export METEOR_NAMESPACE=${ns}
export METEOR_TLS=uwsgd
export METEOR_HOST=${METEOR_VANILLA_HOST}
export NGINX_REPLICAS=${METEOR_VANILLA_REPLICAS}
exec ~/pod/meteor/gw/deploy.sh "${ns}"
