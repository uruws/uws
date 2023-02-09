#!/bin/sh
set -eu

PROXY_VERSION=$(cat ~/k8s/nginx/VERSION)
export PROXY_VERSION

PROXY_REPLICAS=${NGINX_REPLICAS:-3}
export PROXY_REPLICAS
PROXY_CPU=${NGINX_CPU:-400}
export PROXY_CPU
PROXY_MEM=${NGINX_MEM:-1500}
export PROXY_MEM

~/k8s/nginx/configure.sh

envsubst <~/k8s/nginx/deploy.yaml | uwskube apply -n nginx -f -

exit 0
