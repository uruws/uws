#!/bin/sh
set -u
~/k8s/haproxy/rollin.sh pod/tapo/srmnt/cdn
~/k8s/haproxy/rollin.sh pod/tapo/srmnt
exit 0
