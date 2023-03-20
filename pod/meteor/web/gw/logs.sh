#!/bin/sh
set -eu
ns=web
exec ~/pod/meteor/gw/logs.sh "${ns}" "$@"
