#!/bin/sh
set -eu
ns=${1:?'namespace?'}
opts=${2:-'all'}
uwskube get ${opts} -n ${ns}
echo
echo 'DEPLOY ENV'
~/pod/lib/getcfg.sh ${ns}
exit 0
