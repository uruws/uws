#!/bin/sh
set -eu
cd /home/uws/deploy
git fetch --all
git checkout ${newrev}
exit 0
