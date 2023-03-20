#!/bin/sh
set -eu
ns=worker
exec ~/pod/meteor/gw/setup.sh "${ns}"
