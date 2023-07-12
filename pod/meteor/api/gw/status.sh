#!/bin/sh
set -eu
ns=api
exec ~/pod/meteor/gw/status.sh "${ns}"
