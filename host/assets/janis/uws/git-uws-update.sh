#!/bin/sh
set -eu
refname="$1"
oldrev="$2"
newrev="$3"
export NQDIR=/home/uws/nq
echo "i - NQ $(nq -c /uws/git-uws-deploy.sh ${refname} ${oldrev} ${newrev})"
exit 0
