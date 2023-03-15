#!/bin/sh
set -eu
replicas=${1:?'replicas?'}
ns=worker
exec ~/pod/meteor/gw/scale.sh "${ns}" "${replicas}"
