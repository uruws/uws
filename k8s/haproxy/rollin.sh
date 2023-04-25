#!/bin/sh
set -u
prof=${1:?'haproxy profile?'}
exec ~/k8s/haproxy/ingress/rollin.sh "${prof}"
