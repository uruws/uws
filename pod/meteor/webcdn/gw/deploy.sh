#!/bin/sh
set -eu
ns=webcdn
export METEOR_NAMESPACE=${ns}
export METEOR_TLS=${APPCDN_TLS}
export METEOR_HOST=${APPCDN_HOSTNAME}
export NGINX_REPLICAS=${APPCDN_NGINX_REPLICAS}
export METEOR_NGINX_CONF=${HOME}/pod/meteor/webcdn/nginx.conf
exec ~/pod/meteor/gw/deploy.sh "${ns}"
