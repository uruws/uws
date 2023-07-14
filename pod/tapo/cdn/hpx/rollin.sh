#!/bin/sh
set -u
exec ~/k8s/haproxy/rollin.sh pod/tapo/cdn/hpx
