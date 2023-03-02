#!/bin/sh
set -eu
replicas=${1:?'replicas?'}
~/pod/lib/scale.sh cs meteor "${replicas}"
~/pod/meteor/cs/gw/scale.sh "${replicas}"
exit 0
