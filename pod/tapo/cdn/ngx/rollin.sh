#!/bin/sh
set -eu
export METEOR_NAMESPACE=${TAPO_CDN_NAMESPACE}
export METEOR_TLS=${TAPO_CDN_TLS}
export METEOR_HOST=${TAPO_CDN_HOSTNAME}
export NGINX_REPLICAS=${TAPO_CDN_REPLICAS}
exec ~/pod/tapo/ngx/rollin.sh "${ns}" tapo/cdn
