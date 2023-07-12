#!/bin/sh
set -u
~/pod/test/rollin.sh
exec ~/k8s/haproxy/rollin.sh k8s/gateway/hpx
