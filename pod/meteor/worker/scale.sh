#!/bin/sh
set -eu
replicas=${1:?'replicas?'}
~/pod/lib/scale.sh worker meteor "${replicas}"
exit 0
