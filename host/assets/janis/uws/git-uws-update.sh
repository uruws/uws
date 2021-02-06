#!/bin/sh
set -eux
refname="$1"
oldrev="$2"
newrev="$3"
export NQDIR=/home/uws/nq
nq -c /uws/git-uws-deploy.sh ${newrev}
exit 0
