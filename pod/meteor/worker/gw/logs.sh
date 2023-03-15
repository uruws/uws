#!/bin/sh
set -eu
ns=worker
exec ~/pod/meteor/gw/logs.sh "${ns}" "$@"
