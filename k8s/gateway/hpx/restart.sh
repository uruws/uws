#!/bin/sh
set -eu
exec ~/k8s/haproxy/restart.sh k8s/gateway/hpx
