#!/bin/sh
set -eu
ns=${1:?'app namespace?'}
app=${2:?'app name?'}
uwskube get ${opts} -n "${ns}"
echo
echo 'DEPLOY ENV'
~/pod/meteor/getcfg.sh "${ns}" "${app}"
exit 0
