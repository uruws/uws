#!/bin/sh
set -eu
exec ~/k8s/haproxy/setup.sh pod/meteor/infra-ui
