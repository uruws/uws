#!/bin/sh
set -eu
replicas=${1:?'app replicas?'}
exec ~/pod/tapo/scale.sh tapo web "${replicas}"
