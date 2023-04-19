#!/bin/sh
set -eu
exec ~/k8s/haproxy/backend-logs.sh default "$@"
