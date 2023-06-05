#!/bin/sh
set -u
exec ~/k8s/haproxy/teardown.sh pod/meteor/infra-ui
