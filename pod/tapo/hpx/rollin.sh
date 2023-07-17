#!/bin/sh
set -u
~/k8s/haproxy/rollin.sh pod/tapo/web
~/k8s/haproxy/rollin.sh pod/tapo/cdn
~/k8s/haproxy/rollin.sh pod/tapo/api
exit 0
