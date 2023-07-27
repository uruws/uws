#!/bin/sh
set -eu
~/k8s/haproxy/restart.sh pod/tapo/srmnt/cdn
~/k8s/haproxy/restart.sh pod/tapo/srmnt
exit 0
