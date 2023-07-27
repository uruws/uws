#!/bin/sh
set -eu
exec ~/k8s/haproxy/deploy.sh pod/tapo/srmnt
