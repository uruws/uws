#!/bin/sh
set -eu
ns="${1:?'haproxy namespace?'}hpx"
shift
exec ~/pod/lib/top.sh "${ns}"
