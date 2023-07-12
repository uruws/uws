#!/bin/sh
set -u
ns=${1:?'namespace?'}
exec ~/k8s/efs/rmfs.sh "${ns}" nginx-cache
