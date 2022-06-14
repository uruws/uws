#!/bin/sh
set -eu
# eks-2203
docker build --rm -t uws/eks-2203 \
	-f docker/eks/Dockerfile.2203 \
	./docker/eks
# eks-122-2203
docker build --rm -t uws/eks-122-2203 \
	-f docker/eks/Dockerfile-122.2203 \
	./docker/eks
# eks-k8s-2203 (used for k8sctl)
docker build --rm -t uws/eks-k8s-2203 \
	-f docker/eks/Dockerfile-k8s.2203 \
	./docker/eks
exit 0
