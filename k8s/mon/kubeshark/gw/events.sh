#!/bin/sh
set -eu
exec ~/k8s/nginx/events.sh ksgw "$@"
