#!/bin/sh
set -eu

k8s=${PWD}/k8s
pod=${PWD}/pod

exec docker run -it --rm --name k8s-devel \
	--hostname k8s-devel.uws.local -u uws \
	-v ${k8s}:/home/uws/k8s:ro \
	-v ${pod}:/home/uws/pod:ro \
	uws/k8s:devel $@
