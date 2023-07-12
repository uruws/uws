#!/bin/sh
set -eu
ns=${1:?'namespace?'}
exec ~/k8s/efs/mkfs.sh "${ns}" nginx-cache
