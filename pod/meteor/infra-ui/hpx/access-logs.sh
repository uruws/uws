#!/bin/sh
set -eu
exec ~/k8s/haproxy/access-logs.sh pod/meteor/infra-ui "$@"
