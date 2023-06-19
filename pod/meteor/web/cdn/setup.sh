#!/bin/sh
set -eu
ns=webcdn
uwskube create namespace "${ns}"
exec ~/pod/meteor/gw/setup.sh "${ns}"
