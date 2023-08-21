#!/bin/sh
set -eu
export METEOR_NAMESPACE=${TAPO_API_NAMESPACE}
export METEOR_TLS=${TAPO_API_TLS}
export METEOR_HOST=${TAPO_API_HOSTNAME}
export NGINX_REPLICAS=${TAPO_API_REPLICAS}
exec ~/pod/tapo/ngx/deploy.sh "${ns}" tapo/api
