#!/bin/sh
set -eu
newrev=${1}
umask 0027
export GIT_DIR=.git
cd /home/uws/deploy
git fetch --all
git checkout ${newrev}
echo "hola mundo"
exit 0
