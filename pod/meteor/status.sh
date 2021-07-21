#!/bin/sh
set -eu
app=${1:?'app name?'}
opts=${2:-'all'}
uwskube get ${opts} -n ${app}
echo
echo 'DEPLOY ENV'
~/pod/meteor/getcfg.sh ${app}
exit 0
