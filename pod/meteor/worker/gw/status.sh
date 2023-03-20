#!/bin/sh
set -eu
ns=worker
exec ~/pod/meteor/gw/status.sh "${ns}"
