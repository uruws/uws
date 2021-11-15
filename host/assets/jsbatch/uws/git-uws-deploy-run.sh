#!/bin/sh
set -u

refname="$1"
oldrev="$2"
newrev="$3"

umask 0027
logf=/var/tmp/uws-deploy.log

/uws/git-uws-deploy.sh "${refname}" "${oldrev}" "${newrev}" 2>&1 | tee ${logf}
exit_status=$?

if test "X${exit_status}" != 'X0'; then
	mailx -s '[FAIL] uws deploy' munin-alert <${logf}
fi

exit ${exit_status}
