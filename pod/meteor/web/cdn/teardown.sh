#!/bin/sh
set -u
ns=webcdn
exec ~/pod/meteor/gw/teardown.sh "${ns}"
