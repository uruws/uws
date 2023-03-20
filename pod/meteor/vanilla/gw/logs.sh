#!/bin/sh
set -eu
ns=meteor-vanilla
exec ~/pod/meteor/gw/logs.sh "${ns}" "$@"
