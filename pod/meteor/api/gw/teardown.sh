#!/bin/sh
set -u
ns=api
exec ~/pod/meteor/gw/teardown.sh "${ns}"
