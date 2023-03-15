#!/bin/sh
set -u
ns=web
exec ~/pod/meteor/gw/teardown.sh "${ns}"
