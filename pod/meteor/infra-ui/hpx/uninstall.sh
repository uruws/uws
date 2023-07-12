#!/bin/sh
set -u
exec ~/k8s/haproxy/uninstall.sh pod/meteor/infra-ui
