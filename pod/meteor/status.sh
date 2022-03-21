#!/bin/sh
set -eu
ns=${1:?'app namespace?'}
opts=${2:-'all'}
uwskube get ${opts} -n "${ns}"
echo
echo 'DEPLOY ENV'
~/pod/meteor/getcfg.sh "${ns}"
exit 0
