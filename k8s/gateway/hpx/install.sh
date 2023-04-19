#!/bin/sh
set -eu
exec ~/k8s/haproxy/install.sh ${HOME}/k8s/gateway/hpx/haproxy.env
