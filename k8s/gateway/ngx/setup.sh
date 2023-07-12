#!/bin/sh
set -eu
~/k8s/nginx/setup.sh default
exec ~/k8s/gateway/ngx/deploy.sh
