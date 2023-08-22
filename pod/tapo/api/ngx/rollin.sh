#!/bin/sh
set -eu
ns=${TAPO_API_NAMESPACE}
export METEOR_NAMESPACE=${ns}
export METEOR_TLS=${TAPO_API_TLS}
export METEOR_HOST=${TAPO_API_HOSTNAME}
export NGINX_REPLICAS=${TAPO_API_REPLICAS}
exec ~/pod/tapo/ngx/rollin.sh "${ns}" tapo/api
