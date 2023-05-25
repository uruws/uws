#!/bin/sh
set -eu
ns=${1:?'namespace?'}

cmd=${UWSPOD_GETCFG:-lib/getcfg}

echo "*** rollback get cur version: ${cmd}"

./pod/${cmd}.sh "${ns}" |
	fgrep APP_VERSION       |
	sed 's/^export //'      |
	cut -d '=' -f 2         |
	tr -d "'"

exit 0
