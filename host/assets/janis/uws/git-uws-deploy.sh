#!/bin/sh
set -eu

newrev=${1}
umask 0027

cd /srv/uws/deploy
export GIT_DIR=.git

git fetch --all
git checkout ${newrev}

make awscli
make ecr-login

./env/make.sh prod all
./env/make.sh prod publish

./host/deploy.sh local janis

make clean prune
exit 0
