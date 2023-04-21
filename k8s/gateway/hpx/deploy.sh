#!/bin/sh
set -eu
~/pod/test/deploy.sh
exec ~/k8s/haproxy/ingress/deploy.sh \
	${HOME}/k8s/gateway/hpx/haproxy.env \
	${HOME}/k8s/gateway/hpx/ingress.yaml
