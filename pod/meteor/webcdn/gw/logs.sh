#!/bin/sh
set -eu
ns=webcdn
exec ~/pod/meteor/gw/logs.sh "${ns}" "$@"
