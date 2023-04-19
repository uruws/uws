#!/bin/sh
set -u
exec ~/k8s/haproxy/uninstall.sh ${HOME}/k8s/gateway/hpx/haproxy.env
