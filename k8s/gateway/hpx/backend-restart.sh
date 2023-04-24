#!/bin/sh
set -eu
exec ~/k8s/haproxy/backend-restart.sh k8s/gateway/hpx
