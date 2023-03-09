#!/bin/sh
set -eu
replicas=${1:?'replicas?'}
~/pod/lib/scale.sh api meteor "${replicas}"
exit 0
