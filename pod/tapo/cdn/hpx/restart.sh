#!/bin/sh
set -eu
exec ~/k8s/haproxy/restart.sh pod/tapo/cdn/hpx
