#!/bin/sh
set -eu
replicas=${1:?'replicas?'}
~/pod/lib/scale.sh web meteor "${replicas}"
~/pod/meteor/web/gw/scale.sh "${replicas}"
exit 0
