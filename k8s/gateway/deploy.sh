#!/bin/sh
set -eu
exec ~/k8s/nginx/deploy.sh default k8s/gateway
