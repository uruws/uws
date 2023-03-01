#!/bin/sh
set -eu
ns=cs
# shellcheck source=/home/uws/pod/meteor/gw/configure.sh
. ~/pod/meteor/gw/configure.sh
exec ~/pod/meteor/gw/restart.sh "${ns}"
