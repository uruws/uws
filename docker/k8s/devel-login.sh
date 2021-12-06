#!/bin/sh
set -eu

k8s=${PWD}/k8s
pod=${PWD}/pod

install -v -d -m 0750 ${PWD}/tmp/k8s

exec docker run -it --rm --name k8s-devel-login \
	--hostname k8s-devel.uws.local -u uws \
	-e PYTHONPATH=/home/uws/pod/lib \
	-v ${k8s}:/home/uws/k8s:ro \
	-v ${pod}:/home/uws/pod:ro \
	-v ${PWD}/tmp/k8s:/home/uws/tmp \
	uws/k8s:devel $@
