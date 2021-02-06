#!/bin/sh
set -eu
newrev=${1}
cd /home/uws/deploy
git fetch --all
git checkout ${newrev}
exit 0
