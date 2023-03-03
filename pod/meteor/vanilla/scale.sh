#!/bin/sh
set -eu
replicas=${1:?'replicas?'}
~/pod/lib/scale.sh meteor-vanilla meteor "${replicas}"
~/pod/meteor/vanilla/gw/scale.sh "${replicas}"
exit 0
