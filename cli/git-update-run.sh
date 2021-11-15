#!/bin/sh
set -eu

REPO=${1:?'repo path?'}
REFNAME=${2:?'refname?'}

rname=$(basename ${REPO} .git)

logid=$(date '+%y%m%d-%H%M%S')

logsd=${HOME}/logs
logsf=${logsd}/deploy-${rname}-${logid}.log

mkdir -p -m 0750 ${logsd}

echo "*** START: $(date -R)" >>${logsf}
set +e
echo "*** LOGID: ${logid}" >>${logsf}
echo "*** REPO: ${REPO}" >>${logsf}
echo "*** REFNAME: ${REFNAME}" >>${logsf}

/srv/uws/deploy/cli/git_deploy.py --repo "${REPO}" --tagref "${REFNAME}" >>${logsf}
deploy_rc=$?

echo "*** EXIT STATUS: ${deploy_rc}" >>${logsf}
echo "*** END: $(date -R)" >>${logsf}

if test "X${deploy_rc}" != 'X0'; then
	cat ${logsf} | mailx -s "[FAIL] ${rname} git deploy" munin-alert
fi

exit ${deploy_rc}
