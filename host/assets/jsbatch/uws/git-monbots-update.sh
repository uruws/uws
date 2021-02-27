#!/bin/sh
set -eu
refname="$1"
oldrev="$2"
newrev="$3"
if test 'Xrefs/heads/master' = "X${refname}"; then
	export NQDIR=/home/uwsrun/nq
	echo "i - NQ $(nq -c /uws/git-monbots-deploy.sh "${refname}" "${oldrev}" "${newrev}")"
else
	echo "ERROR: ${refname} - invalid branch, not deploying..."
fi
exit 0
