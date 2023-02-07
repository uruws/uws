#!/bin/sh
set -eu

# nginx.env
uwskube delete secret proxy-env -n nginx || true
uwskube create secret generic proxy-env -n nginx \
	--from-env-file=${HOME}/cluster/nginx.env

# sites-enabled
uwskube delete secret sites-enabled -n nginx || true
uwskube create secret generic sites-enabled -n nginx \
	--from-file=${HOME}/cluster/nginx/sites-enabled

exit 0
