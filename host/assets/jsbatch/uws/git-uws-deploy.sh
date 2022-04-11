#!/bin/sh
set -eu

refname="$1"
oldrev="$2"
newrev="$3"

umask 0027

cd /srv/uws/deploy
export GIT_DIR=.git

echo "i - START $(date -R)"
echo "i - git checkout ${refname} ${oldrev} ${newrev}"

#~ git fetch --prune --prune-tags --tags
#~ git checkout "${newrev}"
git pull --quiet --no-rebase --verify-signatures
git status

sleep 1
echo 'i - make deploy'
make deploy AWS_REGION=us-west-1 DEPLOY_SERVER=jsbatch

echo "i - END $(date -R)"
exit 0
