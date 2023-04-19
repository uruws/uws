#!/bin/sh
set -u
exec ~/k8s/haproxy/teardown.sh ${HOME}/k8s/gateway/hpx/haproxy.env
