#!/bin/sh
set -eu
ns=${1:?'namespace?'}
app=${2:?'app name?'}
version=${3:-''}
pod=${HOME}/pod/${app}

if test "X${version}" != 'X'; then
	~/pod/lib/setcfg.sh "${ns}" "${version}"
fi

envf=$(mktemp -p /tmp pod-${ns}-deploy.XXXXXXXX)
~/pod/lib/getcfg.sh "${ns}" >${envf}
cat ${envf}

# shellcheck disable=SC1090
. ${envf}
rm -f ${envf}

envsubst <${pod}/deploy.yaml | uwskube apply -f -

~/pod/lib/rollback-setcfg.sh "${ns}" "${version}"
exit 0
