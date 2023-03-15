#!/bin/sh
set -eu
ns=cs
exec ~/pod/meteor/gw/logs.sh "${ns}" "$@"
