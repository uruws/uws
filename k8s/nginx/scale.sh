#!/bin/sh
set -eu
ns=${1:?'namespace?'}
replicas=${2:?'replicas?'}
exec ~/pod/lib/scale.sh "${ns}" proxy "${replicas}"
