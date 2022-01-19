#!/bin/sh
set -eu
docker build --rm -t uws/ansible:devel \
	-f ./docker/asb/Dockerfile.devel \
	./docker/asb
exit 0
