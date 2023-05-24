#!/bin/sh
set -eu
ns=api
exec ~/pod/meteor/gw/logs.sh "${ns}" "$@"
