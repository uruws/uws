#!/bin/sh
set -eu
exec ~/k8s/haproxy/deploy.sh pod/meteor/infra-ui
