#!/bin/sh
set -u
ns=worker
exec ~/pod/meteor/gw/teardown.sh "${ns}"
