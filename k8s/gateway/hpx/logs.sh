#!/bin/sh
set -eu
exec ~/k8s/haproxy/logs.sh k8s/gateway/hpx "$@"
