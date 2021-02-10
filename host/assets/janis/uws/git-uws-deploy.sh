#!/bin/sh
set -eu

refname="$1"
oldrev="$2"
newrev="$3"

umask 0027
logf=/var/log/uws-deploy.log

cd /srv/uws/deploy
export GIT_DIR=.git

echo "i - START $(date -R)" | tee ${logf}
echo "i - git checkout ${refname} ${oldrev} ${newrev}" | tee -a ${logf}

git fetch --all | tee -a ${logf}
git checkout ${newrev} | tee -a ${logf}

sleep 1
echo 'i - make deploy' | tee -a ${logf}
make deploy | tee -a ${logf}

echo "i - END $(date -R)" | tee -a ${logf}
exit 0
