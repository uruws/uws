#!/bin/sh
set -u
~/pod/test/rollin.sh
~/k8s/haproxy/rollin.sh
exec ~/k8s/haproxy/ingress/rollin.sh \
	${HOME}/k8s/gateway/hpx/haproxy.env \
	${HOME}/k8s/gateway/hpx/ingress.yaml
