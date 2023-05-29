#!/bin/sh
set -eu
replicas=${1:?'replicas?'}
ns=api
exec ~/pod/meteor/gw/scale.sh "${ns}" "${replicas}"
