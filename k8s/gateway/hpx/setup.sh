#!/bin/sh
set -eu
~/k8s/haproxy/setup.sh k8s/gateway/hpx
exec ~/k8s/haproxy/install.sh k8s/gateway/hpx
