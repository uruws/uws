#!/bin/sh
set -eu
uwskube create namespace ksgw
exec ~/k8s/nginx/setup.sh ksgw
