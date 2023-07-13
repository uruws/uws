#!/bin/sh
set -eu
exec ~/k8s/haproxy/status.sh pod/tapo/web/hpx
