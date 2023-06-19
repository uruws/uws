#!/bin/sh
set -eu

appver=${1:-''}
ns=webcdn

export METEOR_NAMESPACE=${ns}
export METEOR_TLS=${APPCDN_TLS}
export METEOR_HOST=${APPCDN_HOSTNAME}
export NGINX_REPLICAS=${APPCDN_NGINX_REPLICAS}
export METEOR_NGINX_CONF=${HOME}/pod/meteor/web/cdn/nginx.conf
~/pod/meteor/gw/deploy.sh "${ns}"

~/pod/meteor/web/cdn/meteor-deploy.sh "${appver}"
exec ~/pod/meteor/web/cdn/meteor-wait.sh