#!/bin/sh
set -eu
ns=${1:?'namespace?'}
shift
exec ~/pod/lib/events.sh "${ns}" "$@"
