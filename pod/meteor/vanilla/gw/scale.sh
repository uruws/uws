#!/bin/sh
set -eu
replicas=${1:?'replicas?'}
ns=meteor-vanilla
exec ~/pod/meteor/gw/scale.sh "${ns}" "${replicas}"
