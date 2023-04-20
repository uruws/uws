#!/bin/sh
set -eu
exec ~/k8s/haproxy/deploy.sh \
	${HOME}/k8s/gateway/hpx/haproxy.env \
	${HOME}/k8s/gateway/hpx/ingress.yaml
