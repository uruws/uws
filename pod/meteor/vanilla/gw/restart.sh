#!/bin/sh
set -eu
ns=meteor-vanilla
export METEOR_NAMESPACE=${ns}
export METEOR_TLS=uwsgd
export METEOR_HOST=${METEOR_VANILLA_HOST}
exec ~/pod/meteor/gw/restart.sh "${ns}"
