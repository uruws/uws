#!/bin/sh
set -eu
replicas=${1:?'replicas?'}
exec ~/pod/lib/scale.sh meteor-vanilla meteor "${replicas}"
