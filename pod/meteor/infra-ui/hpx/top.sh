#!/bin/sh
set -eu
exec ~/k8s/haproxy/top.sh pod/meteor/infra-ui
