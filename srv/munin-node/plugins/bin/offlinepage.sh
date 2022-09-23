#!/bin/sh
set -eu
pldir=/uws/lib/plugins
export PYTHONPATH=${pldir}
exec /usr/bin/python3 -m offlinepage "$@"
