#!/bin/sh
set -eu

logfn=$(mktemp --tmpdir app-autobuild-deploy.XXXXXXXXXX)

exec >${logfn}
exec 2>&1

app=${1:?'app?'}
version=${2:?'version?'}

bindir=${UWSCLI_BINDIR:-'/srv/home/uwscli/bin'}

set +e

${bindir}/app-autobuild "${app}" --deploy "${version}"
rc=$?

set -e

subject="app-autobuild ${app} ${version}"

if test "X${rc}" = '0'; then
	cat ${logfn} | mailx -s "[OK] ${subject}" root
else
	cat ${logfn} | mailx -s "[ERROR] ${subject}" munin-alert
fi

exit ${rc}
