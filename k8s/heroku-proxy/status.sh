#!/bin/sh
set -eu
exec ~/k8s/nginx-ingress/helm/status.sh heroku-proxy "$@"
