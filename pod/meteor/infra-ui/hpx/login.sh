#!/bin/sh
set -eu
exec ~/k8s/haproxy/login.sh pod/meteor/infra-ui
