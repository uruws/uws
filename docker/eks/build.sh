#!/bin/sh
set -eu
# eks
docker build $@ --rm -t uws/eks ./docker/eks
# eks-k8s
docker build $@ --rm -t uws/eks-k8s \
	-f docker/eks/Dockerfile.k8s \
	./docker/eks
exit 0
