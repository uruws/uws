#!/bin/sh
set -eu
ns=worker
exec ~/pod/meteor/gw/top.sh "${ns}"
