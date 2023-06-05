#!/bin/sh
set -eu
exec ~/k8s/haproxy/status.sh pod/meteor/infra-ui
