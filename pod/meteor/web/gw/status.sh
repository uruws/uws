#!/bin/sh
set -eu
ns=web
exec ~/pod/meteor/gw/status.sh "${ns}"
