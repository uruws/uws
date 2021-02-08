#!/bin/sh
set -eu

newrev=${1}
umask 0027

export GIT_DIR=.git

cd /home/uws/deploy

git fetch --all
git checkout ${newrev}

./env/make.sh prod all
./env/make.sh prod publish

./host/deploy.sh local janis

./env/make.sh prod prune
exit 0
