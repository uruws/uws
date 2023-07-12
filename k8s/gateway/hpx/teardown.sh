#!/bin/sh
set -u
exec ~/k8s/haproxy/teardown.sh k8s/gateway/hpx
