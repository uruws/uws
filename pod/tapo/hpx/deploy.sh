#!/bin/sh
set -eu
~/k8s/haproxy/deploy.sh pod/tapo/api
~/k8s/haproxy/deploy.sh pod/tapo/cdn
~/k8s/haproxy/deploy.sh pod/tapo/web
exit 0
