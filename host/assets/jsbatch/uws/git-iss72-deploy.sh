#!/bin/sh
set -eu

refname="$1"
oldrev="$2"
newrev="$3"

umask 0027
logf=/var/tmp/analysis-iss72-deploy.log

cd /srv/deploy/analysis
export GIT_DIR=.git

echo "i - START $(date -R)" | tee ${logf}
echo "i - git checkout ${refname} ${oldrev} ${newrev}" | tee -a ${logf}

git fetch --all 2>&1 | tee -a ${logf}
git checkout ${newrev} 2>&1 | tee -a ${logf}
git status 2>&1 | tee -a ${logf}

echo 'i - build container' | tee -a ${logf}
make -C docker iss72 2>&1 | tee -a ${logf}

echo 'i - dispatch container(s)' | tee -a ${logf}
./docker/iss72/run.sh /home/uwsrun/.analysis/iss72-credentials.json 2>&1 | tee -a ${logf}

echo "i - END $(date -R)" | tee -a ${logf}
exit 0
