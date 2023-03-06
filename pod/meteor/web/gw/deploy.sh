#!/bin/sh
set -eu
ns=web
export METEOR_NAMESPACE=${ns}
export METEOR_TLS=${APP_TLS}
export METEOR_HOST=${APP_HOSTNAME}
NGINX_REPLICAS=$(expr ${APP_REPLICAS} + ${METEOR_API_REPLICAS})
export NGINX_REPLICAS
exec ~/pod/meteor/gw/deploy.sh "${ns}"
