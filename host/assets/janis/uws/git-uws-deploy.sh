#!/bin/sh
set -eu

newrev=${1}
umask 0027

cd /srv/uws/deploy
export GIT_DIR=.git

git fetch --all
git checkout ${newrev}

sleep 1
make deploy

exit 0
