#!/bin/sh
set -eu
exec ~/k8s/haproxy/logs.sh pod/meteor/infra-ui "$@"
