#!/bin/sh
set -eux
refname="$1"
oldrev="$2"
newrev="$3"
cd /home/uws/deploy
git fetch --all
git checkout ${newrev}
exit 0
