#!/bin/sh
set -eu
exec ~/k8s/haproxy/status.sh k8s/gateway/hpx
