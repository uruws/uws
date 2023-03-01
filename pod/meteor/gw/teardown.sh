#!/bin/sh
set -u
ns=${1:?'namespace?'}
exec ~/k8s/nginx/teardown.sh "${ns}"
