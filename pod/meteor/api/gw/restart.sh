#!/bin/sh
set -eu
ns=api
export METEOR_NAMESPACE=${ns}
export METEOR_TLS=${METEOR_API_TLS}
export METEOR_HOST=${METEOR_API_HOSTNAME}
export NGINX_REPLICAS=${METEOR_API_NGINX_REPLICAS}
export METEOR_NGINX_CONF=${HOME}/pod/meteor/api/nginx.conf
exec ~/pod/meteor/gw/restart.sh "${ns}"
