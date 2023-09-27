#!/bin/sh
set -eu
ns=${1:?'namespace?'}
exec ~/pod/lib/watch.py -n "${ns}"
