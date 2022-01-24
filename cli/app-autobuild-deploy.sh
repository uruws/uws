#!/bin/sh
set -eu

logfn=$(mktemp -p /run/uwscli/logs app-autobuild-deploy.XXXXXXXXXX)

app=${1:?'app?'}
version=${2:?'version?'}

bindir=${UWSCLI_BINDIR:-'/srv/home/uwscli/bin'}

set +e

${bindir}/app-autobuild "${app}" --deploy "${version}" | tee ${logfn}
rc=$?

set -e

subject="app-autobuild ${app} ${version}"

if test "X${rc}" != 'X0'; then
	cat ${logfn} | mailx -s "[ERROR] ${subject}" munin-alert
else
	cat ${logfn} | mailx -s "[OK] ${subject}" root
fi

exit ${rc}
