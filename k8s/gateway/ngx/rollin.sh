#!/bin/sh
set -eu
exec ~/k8s/nginx/rollin.sh default k8s/gateway/ngx
