#!/bin/sh
set -eu
exec ~/k8s/haproxy/backend-status.sh k8s/gateway/hpx
