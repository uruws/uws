#!/bin/sh
set -eu
prof=${1:?'haproxy profile?'}
exec ~/k8s/haproxy/ingress/deploy.sh "${prof}"
