#!/bin/sh
set -eu
# eks-122
./docker/eks/122/build.sh
# eks-125
./docker/eks/125/build.sh
exit 0
