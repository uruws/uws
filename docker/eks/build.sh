#!/bin/sh
set -eu
# eks
docker build --rm -t uws/eks \
	-f docker/eks/Dockerfile \
	./docker/eks
# eks-2203
docker build --rm -t uws/eks-2203 \
	-f docker/eks/Dockerfile.2203 \
	./docker/eks
# eks-k8s
docker build --rm -t uws/eks-k8s \
	-f docker/eks/Dockerfile-k8s \
	./docker/eks
# eks-k8s-2203
docker build --rm -t uws/eks-k8s-2203 \
	-f docker/eks/Dockerfile-k8s.2203 \
	./docker/eks
exit 0
