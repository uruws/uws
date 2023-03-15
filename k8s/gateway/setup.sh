#!/bin/sh
set -eu
~/k8s/nginx/setup.sh default
exec ~/k8s/gateway/deploy.sh
