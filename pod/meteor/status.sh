#!/bin/sh
namespace=${APP_NAMESPACE:-''}
set -eu
app=${1:?'app name?'}
opts=${2:-'all'}
if test "X${namespace}" = 'X'; then
	namespace="${app}"
fi
uwskube get ${opts} -n ${namespace}
echo
echo 'DEPLOY ENV'
~/pod/meteor/getcfg.sh ${app}
exit 0
