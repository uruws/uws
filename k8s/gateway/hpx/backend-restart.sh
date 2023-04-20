#!/bin/sh
set -eu
exec ~/k8s/haproxy/backend-restart.sh default
