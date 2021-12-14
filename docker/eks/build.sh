#!/bin/sh
set -eu
# eks
docker build --rm -t uws/eks ./docker/eks
# eks-k8s
docker build --rm -t uws/eks-k8s \
	-f docker/eks/Dockerfile.k8s \
	./docker/eks
# devel
docker build --rm -t uws/eks:devel \
	-f docker/eks/Dockerfile.devel \
	./docker/eks
exit 0
