#!/bin/sh
set -eu
replicas=${1:?'replicas?'}
ns=cs
exec ~/pod/meteor/gw/scale.sh "${ns}" "${replicas}"
