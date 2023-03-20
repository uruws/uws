#!/bin/sh
set -eu
replicas=${1:?'replicas?'}
ns=web
exec ~/pod/meteor/gw/scale.sh "${ns}" "${replicas}"
