#!/bin/sh
set -eu
replicas=${1:?'replicas?'}
~/pod/lib/scale.sh worker meteor "${replicas}"
~/pod/meteor/worker/gw/scale.sh "${replicas}"
exit 0
