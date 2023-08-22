#!/bin/sh
set -eu
ns=${TAPO_NAMESPACE}
export METEOR_NAMESPACE=${ns}
export METEOR_TLS=${TAPO_TLS}
export METEOR_HOST=${TAPO_HOSTNAME}
export NGINX_REPLICAS=${TAPO_REPLICAS}
exec ~/pod/tapo/ngx/rollin.sh "${ns}" tapo/web
