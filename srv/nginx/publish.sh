#!/bin/sh
set -eu
REGIONS='sa-east-1 us-east-1 us-east-2 us-west-1 us-west-2'
NGINX_VERSION=$(cat ./k8s/nginx/VERSION)
for region in ${REGIONS}; do
	./host/ecr-login.sh "${region}"
	./cluster/ecr-push.sh "${region}" uws/nginx-2305 "uws:nginx-${NGINX_VERSION}"
done
exit 0
