#!/bin/sh
set -eu
replicas=${1:?'replicas?'}
ns=web
export METEOR_NAMESPACE="${ns}"
export METEOR_TLS="${APP_TLS}"
export METEOR_HOST="${APP_HOSTNAME}"
export NGINX_REPLICAS="${replicas}"
export METEOR_NGINX_CONF="${HOME}/pod/meteor/web/nginx.conf"
exec ~/pod/meteor/gw/deploy.sh "${ns}"
