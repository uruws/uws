#!/bin/sh
set -eu
replicas=${1:?'replicas?'}
exec ~/pod/lib/scale.sh nlpsvc sentiment-twitter "${replicas}"
