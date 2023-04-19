#!/bin/sh
set -eu
exec ~/k8s/haproxy/setup.sh ${HOME}/k8s/gateway/hpx/haproxy.env
