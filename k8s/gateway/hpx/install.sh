#!/bin/sh
set -eu
exec ~/k8s/haproxy/install.sh k8s/gateway/hpx
