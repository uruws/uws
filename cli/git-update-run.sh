#!/bin/sh
set -eu

REPO=${1:?'repo path?'}
REFNAME=${2:?'refname?'}

rname=$(basename "${REPO}" .git)

logid=$(date '+%y%m%d-%H%M%S')

logsd=${HOME}/logs
logsf=${logsd}/deploy-${rname}-${logid}.log

install -v -d -m 0750 "${logsd}"

exec | tee "${logsf}"
exec 2>&1

echo "*** START: $(date -R)"
set +e
echo "*** LOGID: ${logid}"
echo "*** REPO: ${REPO}"
echo "*** REFNAME: ${REFNAME}"

/srv/uws/deploy/cli/git_deploy.py --repo "${REPO}" --tagref "${REFNAME}"
deploy_rc=$?

echo "*** EXIT STATUS: ${deploy_rc}"
echo "*** END: $(date -R)"

if test "X${deploy_rc}" != 'X0'; then
	mailx -s "[FAIL] ${rname} git deploy" munin-alert <"${logsf}"
fi

exit ${deploy_rc}
