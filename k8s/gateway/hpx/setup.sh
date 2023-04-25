#!/bin/sh
set -eu
exec ~/k8s/haproxy/setup.sh k8s/gateway/hpx
