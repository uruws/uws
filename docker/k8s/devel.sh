#!/bin/sh
set -eu

k8s=${PWD}/k8s
pod=${PWD}/pod
go=${PWD}/go

install -v -d -m 0750 ${PWD}/tmp/k8s

devel_login=${K8S_DEVEL_LOGIN:-'false'}
docker_args='--rm --name k8s-devel'
if test "X${devel_login}" = 'Xtrue'; then
	docker_args='-it --rm --name k8s-devel-login'
fi

exec docker run ${docker_args} \
	--hostname k8s-devel.uws.local -u uws \
	-e PYTHONPATH=/home/uws/pod/lib:/home/uws/k8s/mon/munin-node/plugins \
	-v ${go}:/go/src:ro \
	-v ${k8s}:/home/uws/k8s:ro \
	-v ${pod}:/home/uws/pod:ro \
	-v ${PWD}/tmp/k8s:/home/uws/tmp \
	uws/k8s:devel "$@"
