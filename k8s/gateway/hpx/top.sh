#!/bin/sh
set -eu
exec ~/k8s/haproxy/top.sh k8s/gateway/hpx
