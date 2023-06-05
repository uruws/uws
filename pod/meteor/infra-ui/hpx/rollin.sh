#!/bin/sh
set -u
exec ~/k8s/haproxy/rollin.sh pod/meteor/infra-ui
