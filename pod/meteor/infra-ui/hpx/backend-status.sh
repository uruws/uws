#!/bin/sh
set -eu
exec ~/k8s/haproxy/backend-status.sh pod/meteor/infra-ui
