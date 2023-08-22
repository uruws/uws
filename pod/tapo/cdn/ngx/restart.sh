#!/bin/sh
set -eu
ns=${TAPO_CDN_NAMESPACE}
export METEOR_NAMESPACE=${ns}
export METEOR_TLS=${TAPO_CDN_TLS}
export METEOR_HOST=${TAPO_CDN_HOSTNAME}
export NGINX_REPLICAS=${TAPO_CDN_REPLICAS}
exec ~/pod/tapo/ngx/restart.sh "${ns}" tapo/cdn
