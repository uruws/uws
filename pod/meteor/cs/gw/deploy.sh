#!/bin/sh
set -eu
ns=cs
export METEOR_NAMESPACE=${ns}
export METEOR_TLS=tapo
export METEOR_HOST=${METEOR_CS_HOST}
export NGINX_REPLICAS=${METEOR_CS_REPLICAS}
exec ~/pod/meteor/gw/deploy.sh "${ns}"
