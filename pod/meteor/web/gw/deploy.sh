#!/bin/sh
set -eu
ns=web
export METEOR_NAMESPACE=${ns}
export METEOR_TLS=${APP_TLS}
export METEOR_HOST=${APP_HOSTNAME}
export NGINX_REPLICAS=${APP_NGINX_REPLICAS}
export METEOR_NGINX_CONF=${HOME}/pod/meteor/web/nginx.conf
exec ~/pod/meteor/gw/deploy.sh "${ns}"
