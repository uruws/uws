#!/bin/sh
set -eu
ns=${1:?'namespace?'}
shift
exec ./pod/lib/logs.py -n "${ns}" -l 'app.kubernetes.io/name=offline-page' $@
