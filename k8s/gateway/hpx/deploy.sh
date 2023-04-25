#!/bin/sh
set -eu
~/pod/test/deploy.sh
exec ~/k8s/haproxy/deploy.sh k8s/gateway/hpx
