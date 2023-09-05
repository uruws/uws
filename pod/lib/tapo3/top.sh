#!/bin/sh
set -eu
ns=${1:?'namespace?'}
exec ~/pod/lib/top.sh "${ns}"
