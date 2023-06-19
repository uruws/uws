#!/bin/sh
set -eu
replicas=${1:?'replicas?'}
~/pod/lib/scale.sh webcdn meteor "${replicas}"
exit 0
