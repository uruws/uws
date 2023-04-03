#!/bin/sh
set -eu
exec ~/k8s/nginx/logs.sh ksgw "$@"
