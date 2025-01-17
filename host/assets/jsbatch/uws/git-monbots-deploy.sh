#!/bin/sh
set -eu

refname="$1"
oldrev="$2"
newrev="$3"

umask 0027
logf=/var/tmp/monbots-deploy.log

cd /srv/deploy/monbots
export GIT_DIR=.git

echo "i - START $(date -R)" | tee ${logf}
echo "i - git checkout ${refname} ${oldrev} ${newrev}" | tee -a ${logf}

git fetch --all 2>&1 | tee -a ${logf}
git checkout "${newrev}" 2>&1 | tee -a ${logf}
git status 2>&1 | tee -a ${logf}

echo "i - END $(date -R)" | tee -a ${logf}
exit 0
