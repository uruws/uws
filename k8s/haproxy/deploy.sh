#!/bin/sh
set -eu
prof=${1:?'haproxy profile?'}
~/k8s/haproxy/install.sh "${prof}"
exec ~/k8s/haproxy/ingress/deploy.sh "${prof}"
