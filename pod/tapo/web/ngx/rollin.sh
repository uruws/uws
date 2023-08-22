#!/bin/sh
set -eu
export METEOR_NAMESPACE=${TAPO_NAMESPACE}
export METEOR_TLS=${TAPO_TLS}
export METEOR_HOST=${TAPO_HOSTNAME}
export NGINX_REPLICAS=${TAPO_REPLICAS}
exec ~/pod/tapo/ngx/rollin.sh "${ns}" tapo/web
