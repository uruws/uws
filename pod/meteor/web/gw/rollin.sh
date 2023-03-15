#!/bin/sh
set -eu
ns=web
export METEOR_NAMESPACE=${ns}
export METEOR_TLS=${APP_TLS}
export METEOR_HOST=${APP_HOSTNAME}
exec ~/pod/meteor/gw/rollin.sh "${ns}"
