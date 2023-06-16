#!/bin/sh
set -eu
replicas=${1:?'replicas?'}
ns=webcdn
exec ~/pod/meteor/gw/scale.sh "${ns}" "${replicas}"
