#!/bin/sh
set -eu
ns=${1:?'namespace?'}
pod=${2:?'pod?'}

envf=$(mktemp -p /tmp "pod-${ns}-rollback.XXXXXXXX")
~/pod/lib/rollback-getcfg.sh "${ns}" >${envf}

echo "*** app rollback: ${ns} ${pod}"
cat ${envf}

# shellcheck disable=SC1090
. ${envf}
rm -f ${envf}

exec "${HOME}/pod/${pod}/deploy.sh" "${APP_VERSION}"
