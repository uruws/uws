#!/bin/sh
set -eu
ns=${1:?'namespace?'}
shift
exec uwskube get ev -n ${ns} --sort-by=lastTimestamp "$@"
