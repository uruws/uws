#!/bin/sh
set -eu
ns=webcdn
exec ~/pod/meteor/gw/status.sh "${ns}"
