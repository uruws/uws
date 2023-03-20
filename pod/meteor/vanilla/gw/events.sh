#!/bin/sh
set -eu
ns=meteor-vanilla
exec ~/pod/meteor/gw/events.sh "${ns}" "$@"
